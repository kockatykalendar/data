#!/usr/bin/env python3

import argparse
import json
import os
import shutil
import sys
from collections import defaultdict
from datetime import date, datetime
import re
from typing import Any, Callable, Literal, NamedTuple, Optional, cast

import fastjsonschema  # type: ignore[import-untyped]
import yaml
from fastjsonschema.exceptions import JsonSchemaException, JsonSchemaValueException  # type: ignore[import-untyped]


parser = argparse.ArgumentParser()
parser.add_argument(
    "-d", "--dry", action="store_true", help="Only validate, do not build output files."
)
parser.add_argument(
    "-i", "--allow-ignored-files", action="store_true", help="Do not raise an error when ignored file (without .yml extension) appears in the data."
)
parser.add_argument(
    "-p", "--missing-place-warnings", action="store_true", help="Show warnings about missing places."
)
parser.add_argument(
    "-q", "--quiet", action="store_true", help="Supress all warnings."
)
parser.add_argument(
    "-r", "--recent-warnings-only", action="store_true", help="Only show warnings for events in current and the next (school) year."
)
parser.add_argument(
    "-s", "--error-on-warnings", action="store_true", help="Treat all warnings as errors."
)
parser.add_argument(
    "--report", metavar="FILE", help="Write a Markdown report of all errors and warnings to FILE (always written, even if no problems are found)."
)
args = parser.parse_args()


def school_year_from_date(date: date) -> str:
    if date.month < 9:
        return "%d_%d" % (date.year - 1, date.year % 100)
    return "%d_%d" % (date.year, (date.year + 1) % 100)

def years_from_school_year(school_year: str) -> tuple[int, int]:
    start_year = int(school_year.split("_")[0])
    return (start_year, start_year + 1)

def year_from_directory_name(dir_name: str) -> Optional[str]:
    years: list[str] = re.findall(r"\d{4}", dir_name)
    if len(years) == 0: return None # Root directory
    if len(years) > 1: warn(os.path.join(ROOT, "data", dir_name), "Year string contains more than one year-like number.") # But we should take the first one
    return years[0]


# ---------------------------------------------------------------------------
# Collecting and reporting problems
# ---------------------------------------------------------------------------

class Issue(NamedTuple):
    level: Literal["error", "warning"]
    file: str  # relative to ROOT
    message: str
    line: Optional[int] = None  # only known for YAML syntax errors

    def location(self) -> str:
        return self.file + (":%d" % self.line if self.line else "")


ISSUES: list[Issue] = []

def error(path: str, message: str, line: Optional[int] = None) -> None:
    ISSUES.append(Issue("error", os.path.relpath(path, ROOT), message, line))

def warn(path: str, message: str, year: Optional[int] = None) -> None:
    if args.recent_warnings_only and year is not None and year < CURRENT_YEAR: return
    if args.error_on_warnings: return error(path, message)
    if args.quiet: return
    ISSUES.append(Issue("warning", os.path.relpath(path, ROOT), message))

def yaml_error(path: str, e: yaml.YAMLError) -> None:
    if isinstance(e, yaml.MarkedYAMLError) and e.problem_mark:
        error(path, "Invalid YAML: %s." % e.problem, line=e.problem_mark.line + 1)
    else:
        error(path, "Invalid YAML: %s" % e)

def plural(count: int, word: str) -> str:
    return "%d %s%s" % (count, word, "" if count == 1 else "s")

def print_issues(issues: list[Issue]) -> None:
    def escape_workflow_command(text: str) -> str:
        return text.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
    on_github = os.environ.get("GITHUB_ACTIONS") == "true"
    for issue in issues:
        if on_github:
            # Workflow command, shown as an annotation in the check summary and in "Files changed".
            properties = "file=" + escape_workflow_command(issue.file).replace(":", "%3A").replace(",", "%2C")
            if issue.line: properties += ",line=%d" % issue.line
            print("::%s %s::%s" % (issue.level, properties, escape_workflow_command(issue.message)))
        else:
            color = "31" if issue.level == "error" else "33"
            label = issue.level.capitalize()
            if sys.stdout.isatty(): label = "\033[1;%sm%s\033[0m" % (color, label)
            print("%s in %s:\n\t%s" % (label, issue.location(), issue.message))

def markdown_report(errors: list[Issue], warnings: list[Issue]) -> str:
    if errors:
        status = "errors"
        heading = "❌ Data check found " + plural(len(errors), "error") + (" and " + plural(len(warnings), "warning") if warnings else "")
    elif warnings:
        status = "warnings"
        heading = "⚠️ Data check found " + plural(len(warnings), "warning")
    else:
        return "<!-- data-check-status: ok -->\n### ✅ Data check passed\n\nNo errors or warnings were found.\n"

    lines = ["<!-- data-check-status: %s -->" % status, "### " + heading, "", "| | File | Message |", "|---|---|---|"]
    for issue in errors + warnings:
        icon = "❌" if issue.level == "error" else "⚠️"
        message = issue.message.replace("|", "\\|").replace("\n", " ")
        lines.append("| %s | `%s` | %s |" % (icon, issue.location(), message))
    return "\n".join(lines) + "\n"

def report_and_exit_on_errors() -> None:
    issues = sorted(ISSUES, key=lambda i: (i.level, i.file))
    errors = [i for i in issues if i.level == "error"]
    warnings = [i for i in issues if i.level == "warning"]

    print_issues(warnings + errors)

    report = markdown_report(errors, warnings)
    for report_file, mode in ((args.report, "w"), (os.environ.get("GITHUB_STEP_SUMMARY"), "a")):
        if report_file:
            with open(report_file, mode) as f: f.write(report)

    print("\nValidation %s: %s, %s." % ("failed" if errors else "finished", plural(len(errors), "error"), plural(len(warnings), "warning")))
    if errors: sys.exit(1)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

CURRENT_YEAR = int(school_year_from_date(datetime.now())[:4])

logos = ["icon", "logo"]
DATA_EXTENSIONS = [".yaml", ".yml"]
OUTPUT: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
OUTPUT_ORGANIZERS: dict[str, dict[str, Any]] = {}
ROOT = os.path.dirname(os.path.abspath(__file__))

# fastjsonschema builds the validator with exec(), so static analyzers cannot infer its type.
Validator = Callable[[Any], dict[str, Any]]

with open(os.path.join(ROOT, "schemas", "event.schema.json")) as f:
    validate_event = cast(Validator, fastjsonschema.compile(json.load(f)))

with open(os.path.join(ROOT, "schemas", "organizer.schema.json")) as f:
    validate_organizer = cast(Validator, fastjsonschema.compile(json.load(f)))


print("Validating organizers")

for directory in os.walk(os.path.join(ROOT, "organizers")):
    for file in sorted(directory[2]):
        name, ext = os.path.splitext(file)
        if ext.lower() not in DATA_EXTENSIONS:
            if name[0] == ".": continue # .gitignore, .gitkeep, and other hidden files
            if len(ext.strip()) == 0 and not args.allow_ignored_files:
                error(os.path.join(directory[0], file), "Ignored file in organizers directory.")
            continue
        path = os.path.join(directory[0], file)

        try:
            with open(path) as f:
                organizer_data = validate_organizer(yaml.safe_load(f))
            for logo in logos:
                if logo in organizer_data and not os.path.exists(
                    os.path.join(ROOT, "organizers", organizer_data[logo])
                ):
                    raise JsonSchemaValueException("Invalid path to %s, %s" % (logo, organizer_data[logo]))
            if " - " in organizer_data["name"]:
                warn(path, "Organizer has a hyphen (short dash) in its name, please use '–' (a longer one).")
            OUTPUT_ORGANIZERS[name] = organizer_data
        except yaml.YAMLError as e:
            yaml_error(path, e)
        except JsonSchemaException as e:
            error(path, str(e))

print("Validating events")

for year_directory in sorted(os.listdir(os.path.join(ROOT, "data"))):
    if not os.path.isdir(os.path.join(ROOT, "data", year_directory)): continue
    directory_year_string = year_from_directory_name(year_directory)
    if directory_year_string is None or len(directory_year_string) != 4 or not directory_year_string.isdigit():
        error(os.path.join(ROOT, "data", year_directory), "Directory name does not contain a valid year.")
        continue
    if int(directory_year_string) < CURRENT_YEAR and args.recent_warnings_only:
        print("Skipping past year directory %s in recent-only check." % (year_directory))
        continue
    for directory in sorted(os.walk(os.path.join(ROOT, "data", year_directory))):
        for file in sorted(directory[2]):
            name, ext = os.path.splitext(file)
            if ext.lower() not in DATA_EXTENSIONS:
                if name[0] == ".": continue # .gitignore, .gitkeep, and other hidden files
                if len(ext.strip()) == 0 and not args.allow_ignored_files:
                    error(os.path.join(directory[0], file), "Ignored file appears in data directory.")
                continue
            path = os.path.join(directory[0], file)

            try:
                with open(path) as f:
                    event_data = validate_event(yaml.safe_load(f))
                for organizer in event_data["organizers"]:
                    if organizer not in OUTPUT_ORGANIZERS:
                        raise JsonSchemaValueException("Event organizer %s has no entry in \"organizers\" directory." % (organizer))
                event_date = datetime.strptime(event_data["date"]["start"], "%Y-%m-%d").date()
                event_year = int(school_year_from_date(event_date)[:4])

                directory_year = int(directory_year_string)
                if event_year < directory_year or event_year > directory_year + 1: # Raise an exception, this is certainly a mistake
                    raise JsonSchemaValueException(
                        "Event with date %s is in year %s." % (event_data["date"]["start"], directory_year_string))
                elif event_year == directory_year + 1: # Don't raise an exception, this is quite usual and probably not a mistake
                    warn(path, "Event with date %s is in previous year %s." % (event_data["date"]["start"], directory_year_string), year=directory_year)

                if "end" in event_data["date"].keys():
                    end_date = datetime.strptime(event_data["date"]["end"], "%Y-%m-%d").date()
                    if end_date < event_date:
                        raise JsonSchemaValueException("Event ends before it starts.")

                if not "places" in event_data.keys() or len(event_data["places"]) == 0:
                    if args.missing_place_warnings: warn(path, "Event has missing or empty attribute \"places\".", year=event_year)
                else:
                    for place in event_data["places"]:
                        for forbidden_place in ["TODO", "TO DO", "TBA", "TBD", "?"]:
                            if forbidden_place in place.upper():
                                raise JsonSchemaValueException(
                                    "Event place string \"%s\" containing \"%s\", which is a meaningless placeholder. Remove the places attribute instead." % (place, forbidden_place))
                        if "ONLINE" in place.upper() and not "online" in place:
                            warn(path, "Event has place \"online\" with unconventional capitalization, use all-lowercase.", year=event_year)

                if " - " in event_data["name"]: warn(path, "Event has a hyphen (short dash) in its name, please use '–' (a longer one).", year=event_year)
                if " - " in event_data.get("info", ""): warn(path, "Event has a hyphen (short dash) in its info string, please use '–' (a longer one).", year=event_year)

                if not args.dry: OUTPUT[school_year_from_date(event_date)].append(event_data)
            except yaml.YAMLError as e:
                yaml_error(path, e)
            except JsonSchemaException as e:
                error(path, str(e))

report_and_exit_on_errors()

# ---------------------------------------------------------------------------
# Writing output files
# ---------------------------------------------------------------------------

if not args.dry:
    os.makedirs(os.path.join(ROOT, "build"), exist_ok=True)
    print("Writing output for organizers.")

    for reference, organizer in OUTPUT_ORGANIZERS.items():
        for logo in logos:
            if logo in organizer:
                os.makedirs(
                    os.path.dirname(os.path.join(ROOT, "build", organizer[logo])),
                    exist_ok=True,
                )
                shutil.copy(
                    os.path.join(ROOT, "organizers", organizer[logo]),
                    os.path.join(ROOT, "build", organizer[logo]),
                )

    with open(os.path.join(ROOT, "build/organizers.json"), "w") as f:
        json.dump(OUTPUT_ORGANIZERS, f)

    for year, events in OUTPUT.items():
        print("Writing output for year %s." % (year))

        with open(os.path.join(ROOT, "build", "%s.json" % (year)), "w") as f:
            json.dump(events, f)

    year_index: list[dict[str, Any]] = []
    for year in OUTPUT.keys():
        years = years_from_school_year(year)
        year_index.append(
            {
                "start_year": years[0],
                "end_year": years[1],
                "school_year": "%d/%d" % (years[0], years[1]),
                "filename": "%s.json" % (year,),
            }
        )

    with open(os.path.join(ROOT, "build", "index.json"), "w") as f:
        json.dump(year_index, f)

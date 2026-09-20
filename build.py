#!/usr/bin/env python3

import argparse
import json
import os
import shutil
import sys
from collections import defaultdict, namedtuple
from datetime import date, datetime
import re

import fastjsonschema
import yaml
from fastjsonschema.exceptions import JsonSchemaException, JsonSchemaValueException


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
args = parser.parse_args()


def school_year_from_date(date: date) -> str:
    if date.month < 9:
        return "%d_%d" % (date.year - 1, date.year % 100)
    return "%d_%d" % (date.year, (date.year + 1) % 100)

def years_from_school_year(school_year):
    print(school_year)
    start_year = int(school_year.split("_")[0])
    return (start_year, start_year + 1)

def year_from_directory_name(dir_name):
    years = re.findall(r"\d{4}", dir_name)
    if len(years) == 0: return None # Root directory
    if len(years) > 1: warn(f"String {dir_name} contains more than one year-like number.") # But we should take the first one
    # return datetime.strptime(years[0], "%Y").date()
    return years[0]

ErrorData = namedtuple("ErrorData", ["file", "message"])
ERRORS = []

current_year = int(school_year_from_date(datetime.now())[:4])
def warn(path, message, year=None):
    if args.recent_warnings_only and year is not None and year < current_year: return
    if args.error_on_warnings:
        ERRORS.append(ErrorData(path, message))
        return
    if args.quiet: return
    print("\nWarning in file %s:\n\t%s" % (path, message))

logos = ["icon", "logo"]
DATA_EXTENSIONS = [".yaml", ".yml"]
OUTPUT = defaultdict(lambda: [])
OUTPUT_ORGANIZERS = {}
ROOT = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(ROOT, "schemas", "event.schema.json")) as f:
    validate_event = fastjsonschema.compile(json.load(f))

with open(os.path.join(ROOT, "schemas", "organizer.schema.json")) as f:
    validate_organizer = fastjsonschema.compile(json.load(f))

print("Validating organizers")

for directory in os.walk(os.path.join(ROOT, "organizers")):
    for file in directory[2]:
        name, ext = os.path.splitext(file)
        if ext.lower() not in DATA_EXTENSIONS:
            if name[0] == ".": continue # .gitignore, .gitkeep, and other hidden files
            if len(ext.strip()) == 0 and not args.allow_ignored_files:
                ERRORS.append(ErrorData(os.path.join(directory[0], file), "Ignored file in organizers directory."))
                print("F", end="", flush=True)
            continue
        path = os.path.join(directory[0], file)

        with open(path) as f:
            organizer_data = yaml.safe_load(f)
            try:
                organizer_data = validate_organizer(organizer_data)
                for logo in logos:
                    if logo in organizer_data and not os.path.exists(
                        os.path.join(ROOT, "organizers", organizer_data[logo])
                    ):
                        raise JsonSchemaValueException(
                            "Invalid path to %s, %s" % (logo, organizer_data[logo])
                        )
                if " - " in organizer_data["name"]:
                    warn(path, "Organizer has a hyphen (short dash) in its name, please use '–' (a longer one).")
                OUTPUT_ORGANIZERS[name] = organizer_data
                print(".", end="", flush=True)
            except JsonSchemaException as e:
                ERRORS.append(ErrorData(path, e.message))
                print("F", end="", flush=True)

print("\nValidating events")

for directory in os.walk(os.path.join(ROOT, "data")):
    directory_year_string = year_from_directory_name(directory[0])
    for file in directory[2]:
        name, ext = os.path.splitext(file)
        if ext.lower() not in DATA_EXTENSIONS:
            if name[0] == ".": continue # .gitignore, .gitkeep, and other hidden files
            if len(ext.strip()) == 0 and not args.allow_ignored_files:
                ERRORS.append(ErrorData(os.path.join(directory[0], file), "Ignored file appears in data directory."))
                print("F", end="", flush=True)
            continue
        path = os.path.join(directory[0], file)

        with open(path) as f:
            event_data = yaml.safe_load(f)
            try:
                event_data = validate_event(event_data)
                for organizer in event_data["organizers"]:
                    if organizer not in OUTPUT_ORGANIZERS:
                        raise JsonSchemaValueException("Event organizer %s has no entry in \"organizers\" directory." % (organizer))
                event_date = datetime.strptime(event_data["date"]["start"], "%Y-%m-%d").date()
                event_year = int(school_year_from_date(event_date)[:4])

                if directory_year_string is not None:
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
                print(".", end="", flush=True)
            except JsonSchemaException as e:
                ERRORS.append(ErrorData(path, e.message))
                print("F", end="", flush=True)

print("\n")

if len(ERRORS):
    for error in ERRORS: print("Error in file %s:\n\t%s" % (error.file, error.message))
    sys.exit(1)
else:
    if args.dry: print("Validation successful, no errors found. Please check for relevant warnings above.")

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

    year_index = []
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

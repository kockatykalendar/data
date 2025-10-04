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
    if len(years) > 1: print(f"String {dir_name} contains more than one year-like number.") # But we should take the first one
    # return datetime.strptime(years[0], "%Y").date()
    return years[0]


logos = ["icon", "logo"]
ErrorData = namedtuple("ErrorData", ["file", "message"])
ERRORS = []
OUTPUT = defaultdict(lambda: [])
OUTPUT_ORGANIZERS = {}
ROOT = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser()
parser.add_argument(
    "--dry", action="store_true", help="Only validate, do not build output files."
)
parser.add_argument(
    "--now", action="store_true", help="Only show warnings for events from current (school) year."
)
parser.add_argument(
    "--no-warn", action="store_true", help="Don't show any warnings."
)
parser.add_argument(
    "--no-warn-missing-place", action="store_true", help="Ignore warnings about missing places."
)
args = parser.parse_args()


with open(os.path.join(ROOT, "schemas", "event.schema.json")) as f:
    validate_event = fastjsonschema.compile(json.load(f))

with open(os.path.join(ROOT, "schemas", "organizer.schema.json")) as f:
    validate_organizer = fastjsonschema.compile(json.load(f))

print("validating orgnanizers")

for directory in os.walk(os.path.join(ROOT, "organizers")):
    for file in directory[2]:
        name, ext = os.path.splitext(file)
        if ext.lower() not in [".yaml", ".yml"]:
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
                OUTPUT_ORGANIZERS[name] = organizer_data
                print(".", end="", flush=True)
            except JsonSchemaException as e:
                ERRORS.append(ErrorData(path, e.message))
                print("F", end="", flush=True)

print("\nValidating events")

current_year = int(school_year_from_date(datetime.now())[:4])
for directory in os.walk(os.path.join(ROOT, "data")):
    directory_year_string = year_from_directory_name(directory[0])
    for file in directory[2]:
        name, ext = os.path.splitext(file)
        if ext.lower() not in [".yaml", ".yml"]:
            continue
        path = os.path.join(directory[0], file)

        with open(path) as f:
            event_data = yaml.safe_load(f)
            try:
                event_data = validate_event(event_data)
                for organizer in event_data["organizers"]:
                    if organizer not in OUTPUT_ORGANIZERS:
                        raise JsonSchemaValueException(
                            "Organizer %s is not in organizers." % (organizer)
                        )
                event_date = datetime.strptime(event_data["date"]["start"], "%Y-%m-%d").date()
                event_year = int(school_year_from_date(event_date)[:4])
                
                if directory_year_string is not None:
                    directory_year = int(directory_year_string)
                    if event_year < directory_year:
                        raise JsonSchemaValueException(
                            "Event \"%s\" with date %s is in year %s." % (event_data["name"], event_data["date"]["start"], directory_year_string))
                        # Raise an exception, this is certainly a mistake
                    if event_year > directory_year:
                        if ((not args.now or event_year == current_year) and not args.no_warn):
                            print("\n" + "Event \"%s\" with date %s is in year %s." % (event_data["name"], event_data["date"]["start"], directory_year_string))
                        # Don't raise an exception, this is quite usual and probably not a mistake
                
                if "end" in event_data["date"].keys():
                    end_date = datetime.strptime(event_data["date"]["end"], "%Y-%m-%d").date()
                    if end_date < event_date:
                        raise JsonSchemaValueException("Event \"%s\" ends before it starts." % event_data["name"])

                if not "places" in event_data.keys() or len(event_data["places"]) == 0:
                    if ((not args.now or event_year == current_year) and not args.no_warn and not args.no_warn_missing_place):
                        print("\n" + "Event \"%s\" in year %s has missing or empty attribute \"places\"." % (event_data["name"], event_year))
                
                if not args.dry:
                    OUTPUT[school_year_from_date(event_date)].append(event_data)
                print(".", end="", flush=True)
            except JsonSchemaException as e:
                ERRORS.append(ErrorData(path, e.message))
                print("F", end="", flush=True)

print("\n")

if len(ERRORS):
    for error in ERRORS:
        print("Error validating file %s:\n\t%s" % (error.file, error.message))
    sys.exit(1)

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

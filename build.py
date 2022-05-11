import argparse
import json
import os
import shutil
import sys
from collections import defaultdict, namedtuple
from datetime import date, datetime

import fastjsonschema
import yaml
from fastjsonschema.exceptions import JsonSchemaException, JsonSchemaValueException


def school_year_from_date(date: date) -> str:
    if date.month < 9:
        return "%d_%d" % (date.year - 1, date.year % 100)
    return "%d_%d" % (date.year, (date.year + 1) % 100)


def years_from_school_year(school_year):
    start_year = int(school_year.split("_")[0])
    return (start_year, start_year + 1)


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

for directory in os.walk(os.path.join(ROOT, "data")):
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
                if not args.dry:
                    event_date = datetime.strptime(
                        event_data["date"]["start"], "%Y-%m-%d"
                    ).date()
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

    for reference, organizer in OUTPUT.items():
        for logo in logos:
            if logo in organizer_data:
                os.makedirs(
                    os.path.dirname(os.path.join(ROOT, "build", organizer_data[logo])),
                    exist_ok=True,
                )
                shutil.copy(
                    os.path.join(ROOT, "organizers", organizer_data[logo]),
                    os.path.join(ROOT, "build", organizer_data[logo]),
                )

    with open(os.path.join(ROOT, "build/organizers.json"), "w") as f:
        json.dump(OUTPUT, f)

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

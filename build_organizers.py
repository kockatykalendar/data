import argparse
import json
import os
import sys
import shutil
from collections import defaultdict, namedtuple
from datetime import date, datetime

import fastjsonschema
import yaml
from fastjsonschema.exceptions import JsonSchemaException, JsonSchemaValueException

logos = ["icon", "icon-darkmode", "small-icon", "small-icon-darkmode"]
ErrorData = namedtuple("ErrorData", ["file", "message"])
ERRORS = []
OUTPUT = {}
ROOT = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser()
parser.add_argument(
    "--dry", action="store_true", help="Only validate, do not build output files."
)
args = parser.parse_args()


with open(os.path.join(ROOT, "schemas", "organizer.schema.json")) as f:
    validate_organizer = fastjsonschema.compile(json.load(f))

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
                    if logo in organizer_data and not os.path.exists(os.path.join(ROOT, "organizers", organizer_data[logo])):
                        raise JsonSchemaValueException("Invalid path to %s, %s" % (logo, organizer_data[logo]))
                if not args.dry:
                    OUTPUT[name] = organizer_data
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
                os.makedirs(os.path.dirname(os.path.join(ROOT, "build", organizer_data[logo])), exist_ok=True)
                shutil.copy(os.path.join(ROOT, "organizers", organizer_data[logo]), os.path.join(ROOT, "build", organizer_data[logo]))

    with open(os.path.join(ROOT, "build/organizers.json"), "w") as f:
        json.dump(OUTPUT, f)

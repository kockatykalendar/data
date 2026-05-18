import yaml
from jinja2 import Environment, FileSystemLoader, Template
import argparse
import datetime
from pathlib import Path


import colorama

colorama.init()

parser = argparse.ArgumentParser(
    description="Create rounds of trojsten competitions",
)
parser.add_argument(
    "seminar", choices=["FKS", "KMS", "KSP", "UFO", "PRASK", "FX", "SUSI", "Riešky"]
)
parser.add_argument("year", help="year format eg. 2021_22")
parser.add_argument(
    "dates",
    nargs="+",
    default=[],
    help="dates of rounds in increasing order in format eg. 20.9. 3.10. 15.2 7.5.",
)

args = parser.parse_args()

print(args.dates)

with open(f"seminar/{args.seminar}/seminar.yaml", "r", encoding="utf-8") as f:
    seminar_data = yaml.safe_load(f)

env = Environment(
    loader=FileSystemLoader("."),
    trim_blocks=True,
)
template = env.get_template("seminar/kolo.yaml.jinja")

dir_path = Path(
    f"../data/{args.year}/seminare/{seminar_data['organizer']}/{args.seminar}"
)
dir_path.mkdir(parents=True, exist_ok=True)


for p, part in enumerate(seminar_data["parts"]):
    for round in range(1, seminar_data["rounds"] + 1):
        for v in seminar_data["variations"]:
            title_template = Template(v["title"])
            date = (
                datetime.datetime.strptime(
                    f"{args.dates[round - 1 + (p) * seminar_data['rounds']]}{args.year[:4] if p == 0 else int(args.year[:4]) + 1}",
                    "%d.%m.%Y",
                )
                - datetime.timedelta(days=v["offset"])
            ).strftime("%Y-%m-%d")
            rendered = template.render(
                part=part,
                round=round,
                date=date,
                info=v["info"],
                title=title_template.render(
                    part=part, round=round, date=date, info=v["info"], **seminar_data
                ),
                **seminar_data,
            )
            with open(
                dir_path / f"{p + 1}_{round}{v['name']}.yml",
                "w",
                encoding="utf-8",
            ) as f:
                f.write(rendered)

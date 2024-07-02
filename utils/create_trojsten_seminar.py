import argparse
import datetime
import os

import colorama

colorama.init()

VERSION = "1.00"
DATE = "2021-05-02"

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

parts = 2
rounds = 3
if args.seminar in ["KSP", "FX", "PRASK"]:
    rounds = 2

sciences = {
    "FKS": "fyz",
    "KMS": "mat",
    "KSP": "inf",
    "UFO": "fyz",
    "PRASK": "inf",
    "FX": "fyz",
    "SUSI": "other",
    "Riešky": "mat",
}

min_year = {
    "FKS": "ss1",
    "KMS": "ss1",
    "KSP": "ss1",
    "UFO": "zs7",
    "PRASK": "zs7",
    "FX": "ss1",
    "SUSI": "ss1",
    "Riešky": "zs5",
}

max_year = {
    "FKS": "ss4",
    "KMS": "ss4",
    "KSP": "ss4",
    "UFO": "zs9",
    "PRASK": "ss1",
    "FX": "ss4",
    "SUSI": "null",
    "Riešky": "zs9",
}

url = {
    "FKS": "fks",
    "KMS": "kms",
    "KSP": "ksp",
    "UFO": "ufo.fks",
    "PRASK": "prask.ksp",
    "FX": "fx.fks",
    "SUSI": "susi.trojsten",
    "Riešky": "riesky",
}

info = {
    "FKS": (
        "Fyzikálny korešpondenčný seminár je súťaž v riešení netradičných fyzikálnych"
        " problémov. Pomocou zaujímavých experimentov a situácií z bežného života sa"
        " snažíme ukázať, že fyzika nie je taká nudná, ba dokonca ani taká ťažká, ako"
        " sa občas zdá."
    ),
    "KMS": (
        "Baví ťa matematika? Tak neváhaj a zapoj sa do Korešpondenčného Matematického"
        " Semináru! Ide o individuálnu súťaž pozostávajúcu z 10 úloh, pričom stačí"
        " vyriešiť 5. Vyriešiť úlohu neznamená len nájsť výsledok. Treba aj ukázať,"
        " že nájdený výsledok je správny."
    ),
    "KSP": (
        "Korešpondenčný seminár z programovania je súťaž v riešení algoritmických úloh."
        " Riešiš 5 z 8 úloh podľa tvojho levelu skúseností. Riešenie obvykle pozostáva"
        " z funkčného programu, ktorý stránka automaticky otestuje a textového popisu,"
        " čo program robí."
    ),
    "UFO": "",
    "PRASK": (
        "PRASK je súťaž určená pre všetkých základoškolákov, ktorých zaujíma"
        " matematika, informatika, chceli by sa naučiť programovať, alebo len radi"
        " rozmýšľajú a prijímajú výzvy."
    ),
    "FX": (
        "FX je pre tých, ktorí sa chcú vo svete fyziky pohnúť míľovými krokmi dopredu."
        " Každú úlohu môžeš riešiť iteratívne, t.j. do termínu ju môžeš poslať"
        " niekoľkokrát, pričom vždy dostaneš od nás spätnú väzbu, vďaka ktorej môžeš"
        " riešenie ešte vylepšiť."
    ),
    "SUSI": (
        "Na rozdiel od tradičných šifrovačiek je Súťaž v Šifrovaní určená jednotlivcom."
        " Podľa skúseností riešiš šifry v kategórií Agát, Blýskavica alebo Cíferský cech."
        " V každom kole riešiš 5 šifier a na stránku odovzdávaš heslá, ktoré stránka"
        " automaticky opraví."
    ),
    "Riešky": (
        "Riešky sú individuálna dlhodobá súťaž v riešení netradičných úloh."
        " Pri riešeniach nás zaujíma hlavne postup a myšlienky, ktoré doviedli"
        " riešiteľa k výsledku a napíšeme k nim spätnú väzbu."
        " Odmenou pre najúspešnejších riešiteľov je sústredenie."
    ),
}

susi_outdoor = (
    "Na rozdiel od tradičných šifrovačiek je Súťaž v Šifrovaní určená pre jednotlivcov."
    " V objavnom kole riešiš 5 šifier zameraných na špecifickú tému a na stránku odovzdávaš"
    " heslá, ktoré stránka automaticky opraví."
)

susi_outdoor_doprogramovanie = (
    "Štyri týždne pred koncom kola sa na stránke zverejní malá nápoveda spoločná pre všetky"
    " šifry objavného kola. Po tomto termíne môžeš riešenia šifier odovzdávať za 7 bodov až"
    " do zverejnenia veľkých nápovied."
)

info_doprogramovanie = {
    "KSP": (
        "Po riadnom termíne nastáva fáza doprogramovávania. Počas tejto fázy sa nedajú"
        " odovzdávať slovné popisy, stále sa však dajú získať body za program. Navyše"
        " zverejníme aj vzorové riešenia, ktoré Vám vedia pomôcť úlohu vyriešiť a"
        " úspešne naprogramovať."
    ),
    "SUSI": (
        'Štyri týždne pred koncom kola sa na stránke zverejní prvá sada "malých" nápovied'
        " k jednotlivým šifrám. Po tomto termíne môžeš riešenia šifier odovzdávať za 7"
        " bodov až do zverejnenia veľkých nápovied."
    ),
}

name_doprogramovanie = {"KSP": "Doprogramovanie", "SUSI": "Zverejnenie malej nápovedy"}

info_doprogramovanie2 = {
    "SUSI": (
        'Dva týždne pred koncom kola sa na stránke zverejní aj druhá sada "veľkých" nápovied'
        " k jednotlivým šifrám. Po tomto termíne môžeš riešenia šifier odovzdávať za 5"
        " bodov až do skončenia kola."
    ),
}

start = {
    "SUSI": (
        "Dva týždne pred koncom kola sa na stránke zverejní aj druhá sada takzvaných"
        ' "veľkých" nápovied ku jednotlivým šifrám. Akonáhle sa tak stane, za riešenie'
        " môžte získať maximálne 5 bodov."
    ),
}

name_doprogramovanie2 = {"SUSI": "Zverejnenie veľkej nápovedy"}

i = 0
directory = "riesky" if args.seminar == "Riešky" else args.seminar
os.makedirs(f"../data/{args.year}/seminare/trojsten/{directory}", exist_ok=True)
for part in range(1, parts + 1):
    for r in range(1, rounds + 1):
        round = r
        if r == 3 and args.seminar == "SUSI":
            round = "Outdoor"
        with open(
            f"../data/{args.year}/seminare/trojsten/{directory}/{part}_{round}.yml",
            "w",
            encoding="utf-8",
        ) as f:
            f.write(
                f"""name: {f"Riešky {round}. kolo, {"zimná" if part == 1 else "letná"} séria" if args.seminar == "Riešky" else f"{"Suši" if args.seminar == "SUSI" else args.seminar} – {"Koniec " if args.seminar in start else ""}{"Objavného" if round == "Outdoor" else f'{round}.'} {"kola" if args.seminar in start else "kolo"} {"zimnej" if part == 1 else "letnej"}"} časti
type: seminar
sciences:
  - {sciences[args.seminar]}
date:
  start: "{ datetime.datetime.strptime(f'{args.dates[i]}{args.year[:4] if part == 1 else int(args.year[:4])+1}', '%d.%m.%Y').strftime('%Y-%m-%d')}"
contestants:
  min: {min_year[args.seminar]}
  max: {max_year[args.seminar]}
places:
  - online
organizers:
  - {"riesky" if args.seminar == "Riešky" else "trojsten"}
info: "{susi_outdoor if round == "Outdoor" else info[args.seminar]}"
link: https://{url[args.seminar]}.sk/
"""
            )
        if args.seminar in info_doprogramovanie:
            with open(
                f"../data/{args.year}/seminare/trojsten/{directory}/{part}_{round}_after1.yml",
                "w",
                encoding="utf-8",
            ) as f:
                f.write(
                    f"""name: {"Suši" if args.seminar == "SUSI" else args.seminar} – {name_doprogramovanie[args.seminar]} {"Objavného" if round == "Outdoor" else f'{round}.'} kola {"zimnej" if part == 1 else "letnej"} časti
type: seminar
sciences:
  - {sciences[args.seminar]}
date:
  start: "{ (datetime.datetime.strptime(f'{args.dates[i]}{args.year[:4] if part == 1 else int(args.year[:4])+1}', '%d.%m.%Y') - datetime.timedelta(days=14)).strftime('%Y-%m-%d') if args.seminar == 'SUSI' else (datetime.datetime.strptime(f'{args.dates[i]}{args.year[:4] if part == 1 else int(args.year[:4])+1}', '%d.%m.%Y') + datetime.timedelta(days=14)).strftime('%Y-%m-%d')}"
contestants:
  min: {min_year[args.seminar]}
  max: {max_year[args.seminar]}
places:
  - online
organizers:
  - {"riesky" if args.seminar == "Riešky" else "trojsten"}
info: '{susi_outdoor_doprogramovanie if args.seminar == "SUSI" and round == "Outdoor" else info_doprogramovanie[args.seminar]}'
link: https://{url[args.seminar]}.sk/
"""
                )
        if args.seminar in name_doprogramovanie2:
            with open(
                f"../data/{args.year}/seminare/trojsten/{directory}/{part}_{round}_after2.yml",
                "w",
                encoding="utf-8",
            ) as f:
                f.write(
                    f"""name: {"Suši" if args.seminar == "SUSI" else args.seminar} – {name_doprogramovanie2[args.seminar]} {"Objavného" if round == "Outdoor" else f'{round}.'} kola {"zimnej" if part == 1 else "letnej"} časti
type: seminar
sciences:
  - {sciences[args.seminar]}
date:
  start: "{ (datetime.datetime.strptime(f'{args.dates[i]}{args.year[:4] if part == 1 else int(args.year[:4])+1}', '%d.%m.%Y') - datetime.timedelta(days=7)).strftime('%Y-%m-%d')}"
contestants:
  min: {min_year[args.seminar]}
  max: {max_year[args.seminar]}
places:
  - online
organizers:
  - {"riesky" if args.seminar == "Riešky" else "trojsten"}
info: '{info_doprogramovanie2[args.seminar]}'
link: https://{url[args.seminar]}.sk/
"""
                )
        if args.seminar in start:
            with open(
                f"../data/{args.year}/seminare/trojsten/{directory}/{part}_{round}_start.yml",
                "w",
                encoding="utf-8",
            ) as f:
                f.write(
                    f"""name: {"Suši" if args.seminar == "SUSI" else args.seminar} – Zverejnenie {"Objavného" if round == "Outdoor" else f'{round}.'} kola {"zimnej" if part == 1 else "letnej"} časti
type: seminar
sciences:
  - {sciences[args.seminar]}
date:
  start: "{ (datetime.datetime.strptime(f'{args.dates[i]}{args.year[:4] if part == 1 else int(args.year[:4])+1}', '%d.%m.%Y') - datetime.timedelta(days=42)).strftime('%Y-%m-%d')}"
contestants:
  min: {min_year[args.seminar]}
  max: {max_year[args.seminar]}
places:
  - online
organizers:
  - {"riesky" if args.seminar == "Riešky" else "trojsten"}
info: '{start[args.seminar]}'
link: https://{url[args.seminar]}.sk/
"""
                )
        i += 1

<p align="center">
	<h1 align="center">Dáta</h1>
	<p align="center">💾 Dáta Kockatého Kalendára</p>
</p>


## Pridávanie udalostí

### Priečinky

Každá udalosť má svoj `.yml` súbor v priečinku `data`. Kalendáru v princípe nezáleží, kde sa tento súbor v priečinku nachádza, ale pre prehľadnosť sme zvolili takúto štruktúru:
- Priečinok `data` má podpriečinky, ktoré vyjadrujú školské roky (`2020_21`, `2019_20`...).
  - V priečinku školského roka sú ďalšie podpriečinky podľa typu udalosti (`prednasky`, `seminare`, `sutaze`...).
    - V priečinku `seminare`, má každý seminár vlastný podpriečinok (`trojsten`, `P-MAT`, `Riesky`...). Tieto podpriečinky si už spravujú jednotlivé semináre.
    - Priečinok `sutaze`, sa tiež ďalej delí podľa toho o akú súťaž ide (`MO`, `FO`, `IO`, `Zenit`...).


Priečinky školských rokov sa používajú na kontrolu správneho dátumu udalosti (pozri viac v časti Testovanie správnosti).

### Súbory

YML súbor udalosti má presne definovanú štruktúru, ktorá je [zverejnená tu](https://github.com/kockatykalendar/data/blob/master/schemas/event.schema.json).

Užitočnejší ale pre teba bude [príklad, ako sa používa](https://github.com/kockatykalendar/data/blob/master/example.yml).
Najjednoduchší spôsob, ako vyrobiť novú udalosť, je skopírovať si príklad (`example.yml`) alebo udalosť z minulého roka a zmeniť relevantné údaje.

### Pull-requesty

- Na pridanie udalosti si musíš v gite vyrobiť novú vetvu ("branch", hlavná vetva `master` je totiž chránená).
- Keď pridáš všetky potrebné udalosti, vo webovom rozhraní Githubu vyrob pull-request.
- Môžeš tiež v pravom stĺpci v sekcií Reviewers pridať niekoho z [data-managers](https://github.com/orgs/kockatykalendar/teams/data-managers) tímu,
kto skotroluje a akceptuje zmeny (inak môže chvíľu trvať, kým si tvoj pull-request niekto všimne).


## Pridávanie organizátorov

Každý organizátor má svoj `.yml` súbor v priečinku `organizers`. Kalendáru nezáleží, kde sa tento súbor v priečinku nachádza, ale zatiaľ ich dávame priamo do tohoto priečinku.
Taktiež v tomto priečinku môžu byť uložené `logo` a `icon` (malé logo) organizátora, na ktoré treba v `.yml` súbore uviesť relatívny odkaz.


## Buildovanie a kontrola výstupných súborov

**Build nemusíš robiť, deje sa automaticky pri aktualizácií kalendára.**
Testy zároveň bežia pre každý pull-request, takže o prípadných chybách sa dozvieš.
Ale môže to byť užitočné na nájdenie prípadných chýb skôr, než ich nahráš.

Najprv potrebuješ `Python 3`, `pip` a knižnice, ktoré nainštaluješ pomocou `pip install -r requirements.txt`.

Teraz môžeš zbuildiť výstupné súbory pomocou `python build.py`. Výstup sa objaví v priečinku `build`.

### Testovanie správnosti

Ak chceš iba skontrolovať, či sú YML súbory správne, môžeš spustiť `python build.py --dry`.

`build.py` má zopár ďalších nastavení súvisiacich s testovaním, tie si môžeš pozrieť pomocou `python build.py -h`.


## VSCode

Ak používaš Visual Studio Code na úpravu dát, odporúčame si nainštalovať [YAML extension](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml). Potom v nastaveniach projektu (`.vscode/settings.json`) môžeš zadefinovať, že chceš používať schému a aktivuješ si tak autocomplete:

```json
{
    "yaml.schemas": {
        "./schemas/event.schema.json": ["/data/*.yaml", "/data/*.yml"],
        "./schemas/organizers.schema.json": ["/organizers/*.yaml", "/organizers/*.yml"],
    }
}
```

<p align="center">
	<h1 align="center">Dáta</h1>
	<p align="center">💾 Dáta Kockatého Kalendára</p>
</p>


## Pridávanie udalostí

Každá udalosť má svoj `.yml` súbor v priečinku `data`. Kalendáru nezáleží, kde sa tento súbor v priečinku nachádza, ale pre prehľadnosť sme zvolili takúto štruktúru:
Priečinok `data` má podpriečinky, ktoré vyjadrujú školské roky (`2020_21`, `2019_20`...). V priečinku školského roka sú ďalšie podpriečinky podľa mesiaca. Aby sa zoraďovali
správne, pred názov mesiaca sme pridali jeho poradovú číslovku v danom školskom roku (t.j. `01_september`, `02_october`...)

YML súbor udalosti má presne definovanú štruktúru, ktorá je [zverejnená tu](https://github.com/kockatykalendar/data/blob/master/schemas/event.schema.json).
Príklad, ako sa používa si môžeš [pozrieť tu](https://github.com/kockatykalendar/data/blob/master/example.yml).


## Pridávanie organizátorov

Každý organizátor má svoj `.yml` súbor v priečinku `organizers`. Kalendáru nezáleží, kde sa tento súbor v priečinku nachádza, ale zatiaľ ich dávame priamo do tohoto priečinku.
Taktiež v tomto priečinku môžu byť uložené `logo` a `icon` (malé logo) organizátora, s tým, že v `.yml` súbore 

YML súbor udalosti má presne definovanú štruktúru, ktorá je [zverejnená tu](https://github.com/kockatykalendar/data/blob/master/schemas/organizer.schema.json).


## VSCode

Ak používaš VSCode na úpravu dát, odporúčame si nainštalovať [YAML extension](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml). Potom v nastaveniach projektu (`.vscode/settings.json`) môžeš zadefinovať, že chceš používať schému a aktivuješ si tak autocomplete:

```json
{
    "yaml.schemas": {
        "./schemas/event.schema.json": ["/data/*.yaml", "/data/*.yml"],
        "./schemas/organizers.schema.json": ["/organizers/*.yaml", "/organizers/*.yml"],
    }
}
```


## Buildovanie výstupných súborov

**Toto nemusíš robiť, deje sa to automaticky pri aktualizácií kalendára.** Ale keby si predsalen chcel, je to jednoduché.

1. Najprv potrebuješ Python 3 a potrebné knižnice, ktoré nainštaluješ pomocou `pip install -r requirements.txt`.
2. Teraz môžeš vybuildovať výstupné súbory pomocou `python build.py`. Výstup sa objaví v priečinku `build`.

Ak chceš iba skontrolovať, či sú YML súbory dobré, môžeš spustiť `python build.py --dry`.

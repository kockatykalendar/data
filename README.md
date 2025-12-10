<p align="center">
	<h1 align="center">Dáta</h1>
	<p align="center">💾 Dáta Kockatého Kalendára</p>
</p>


## Pridávanie udalostí

### Prístupové práva

Ak chceš pridávať udalosti, máš dve možnosti:
- Preferovaná možnost: Pridať sa do [data-contributors](https://github.com/orgs/kockatykalendar/teams/data-contributors) tímu,
tak, že kontaktuješ niekoho z [data-managers](https://github.com/orgs/kockatykalendar/teams/data-managers),
napríklad [Jančiho](https://github.com/Jajopi), prípadne [Krtka](https://github.com/krtko1). *Tímy sú viditeľné iba pre ľudí v tímoch.*
- Spraviť si fork a z neho spraviť pull-request.

To ti umožní pridávať zmeny nanečisto a vytvárať pull-requesty, ktoré potom niekto z data-managers skontroluje a zverejní.

### Priečinky

Každá udalosť má svoj `.yml` súbor v priečinku `data`. Kalendáru v princípe nezáleží, kde sa tento súbor v priečinku nachádza, ale pre prehľadnosť sme zvolili takúto štruktúru:
- Priečinok `data` má podpriečinky, ktoré vyjadrujú školské roky (`2020_21`, `2019_20`...).
  - V priečinku školského roka sú ďalšie podpriečinky podľa typu udalosti (`prednasky`, `seminare`, `sutaze`, `olympiady`).

Priečinky školských rokov sa používajú na kontrolu správneho dátumu udalosti (pozri viac v časti Testovanie správnosti).

### Súbory

YML súbor udalosti má presne definovanú štruktúru, ktorá je [zverejnená tu](https://github.com/kockatykalendar/data/blob/master/schemas/event.schema.json).

Užitočnejší ale pre teba bude [príklad, ako sa používa](https://github.com/kockatykalendar/data/blob/master/example.yml).
Najjednoduchší spôsob, ako vyrobiť novú udalosť, je skopírovať si príklad (`example.yml`) alebo udalosť z minulého roka a zmeniť relevantné údaje.

### Pull-requesty

- Na pridanie udalosti si musíš v gite vyrobiť novú vetvu ("branch", hlavná vetva `master`, ktorá sa premieta do kalendára, je totiž chránená).
- Keď pridáš všetky potrebné udalosti, vo webovom rozhraní Githubu vyrob pull-request.
- Môžeš tiež v pravom stĺpci v sekcií Reviewers pridať niekoho z [data-managers](https://github.com/orgs/kockatykalendar/teams/data-managers) tímu,
kto skotroluje a akceptuje zmeny (inak by chvíľu trvalo, kým si tvoj pull-request niekto všimne).

### Obsah súborov

Niekoľko užitočných konvencií, ktoré sa oplatí dodrživať, aby jednotlivé udalosti vyzerali konzistentne.

#### Názvy

Pokiaľ sa jedná o kolo konkrétnej súťaže / semináru, názov udalosti by mal obsahovať aj názov súťaže / semináru, nie len dané kolo.
Táto informácia totiž nie je zobrazená na žiadnom inom mieste.
Takže ideálne `KSP - prvé kolo zimnej časti`, nie ~~`Prvé kolo zimnej časti`~~.

Skratky môžu byť aj rozpísané, ale rozpísaním sa znižuje prehľadnosť danej udalosti.
Pokiaľ sú teda skratky dobre známe, neoplatí sa to.

Názov má byť stručný.
Pokiaľ má daná súťaž viac podobných udalostí, chcú byť v názve iba skutočnosti, ktoré sa medzi nimi líšia (napríklad číslo kola),
na všetko ostatné je určený popis.

#### Popisy

Popisy jednotlivých udalostí majú maximálnu dĺžku cca 250 znakov.
To najmä preto, aby na stránke nezaberali priveľa miesta.

Nemal by to však byť problém -- popis má iba vysvetľovať, čo je dána udalosť zač, ak to nie je jasné z nadpisu, prípadne jej robiť reklamu niečim zaujímavým.

Popis nemusí (ba priam nemá) obsahovať:
- Kde a kedy udalosť prebieha -- sú na to samostatné vlastnosti
- Pre koho je udalosť určená (z hľadiska ročníku) -- je na to samostatná vlastnosť
	- Informácia, že udalosť má aj "open" kategóriu bez vekového obmedzenia, sa naopak do popisu hodí
- Akej oblasti (vedy) sa udalosť týka -- je na to samostatná vlastnosť
	- Pokiaľ je to oblasť, ktorú nemáme zahrnutú vo výbere, teda `other`, tak sa naopak táto informácia do popisu hodí 
 	- Pokiaľ je súťaž multiodborová, môže byť táto informácia v popise relevantná
- Pravidlá súťaže, podrobný priebeh -- na to existuje odkaz na stránku súťaže, kde si vie pravidlá ktokoľvek nájsť

Ak si s popisom nevieš rady, kľudne nenapíš nič, alebo proste napíš niečo, a nejaký data-manager to upraví alebo ti povie, čo zmeniť.

#### Miesta

Vlastnosť miesta je po novom nepovinná.

Pokiaľ udalosť prebieha online, konvencia je napísať `online` (s malým písmenom).
Pokiaľ miesto nie je známe alebo nie je dôležité, vlastnosť sa vynecháva (takže prosím žiadne `TODO`, `TBA`, `TO DO`, `TRAMTADADÁ` a podobne -- DO zo slova TODO už nikdy nikto ne-).

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

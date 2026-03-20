<p align="center">
	<h1 align="center">💾 Dáta Kockatého Kalendára</h1>
</p>

Tento repozitár slúži ako zdroj údajov o všetkých udalostiach, ktoré sa zobrazujú v Kockatom Kalendári.

<hr>

V tomto návode sa dozvieš, ako do Kalendára pridávať nové udalosti (a organizátorov).

Pokiaľ nevieš pracovať s gitom alebo Githubom, odporúčame si prečítať
[jednoduchý tutoriál na prácu s Githubom](https://docs.github.com/en/get-started/start-your-journey/hello-world)
alebo
[komplexnejší tutoriál, Github + git](https://www.freecodecamp.org/news/guide-to-git-github-for-beginners-and-experienced-devs/).

## Pridávanie udalostí

### Prístupové práva

Ak chceš pridávať udalosti, máš dve možnosti:
- Preferovaná možnost: Pridať sa do [data-contributors](https://github.com/orgs/kockatykalendar/teams/data-contributors) tímu,
  tak, že kontaktuješ niekoho z [data-managers](https://github.com/orgs/kockatykalendar/teams/data-managers),
  napríklad [Jančiho](https://github.com/Jajopi) ([mail](jan.plachy+kk@trojsten.sk)),
  prípadne [Krtka](https://github.com/krtko1), a dáš nám vedieť, aký máš Github username. *Tímy sú viditeľné iba pre ľudí v tímoch.*
- Druhá možnosť: Spraviť si fork repozitára.

To ti umožní pridávať zmeny nanečisto, teda vytvárať nové branche ("vetvy")
a vytvárať z nich pull-requesty ("žiadosti o zlúčenie") do hlavnej vetvy `master`, ktorá sa zverejňuje.
Tvoje zmeny potom niekto z [data-managers](https://github.com/orgs/kockatykalendar/teams/data-managers) skontroluje a zverejní.

### Pull-requesty

- Na pridanie udalosti si musíš v gite vyrobiť novú vetvu ("branch", hlavná vetva `master`, ktorá sa premieta do Kalendára, je totiž chránená).
- Keď pridáš všetky potrebné udalosti, vo webovom rozhraní Githubu vyrob pull-request.
- Môžeš tiež v pravom stĺpci v sekcií Reviewers pridať niekoho z [data-managers](https://github.com/orgs/kockatykalendar/teams/data-managers) tímu,
aby skotroloval a schválil zmeny (inak bude chvíľu trvať, kým si tvoj pull-request niekto všimne).

#### Pull-request sa sťažuje

Ak pri pull-requeste po submitnutí nevidíš zelenú fajku, ale červený, krížik, v súboroch je niečo zle a treba to opravť ďalšími commitmi.

Klikaním na červené krížiky, dokým sa to dá, a potom na `details`, sa dostaneš k masívnemu bloku textu rozdelenému podľa jednotlivých operácii, ktoré github robil na overenie obsahu. Väčšina z nich je nepodstatná, dôležité hlášky sú tie, ktorými text končí pred vypísaním chyby (sú po anglicky). Konkrétne tam bude veľa bodiek `.`, občas prerušených sťažnosťami na veci, ktoré môžu alebo nemusia byť chyby, a zoznam kritických chýb vypísaných na konci.

Malo by z nich byť zrejmé, aký je so súbormi problém. Ak nie, pingni niekoho z data-managers a sťažuj sa v komentároch k pull-requestu.

### Priečinky

Každá udalosť má svoj YAML (`.yml`) súbor v priečinku `data`.

Pre prehľadnosť sme zvolili takúto štruktúru:
- Priečinok `data` má podpriečinky pre jednotlivé školské roky (`2024_25`, `2025_26`...).
  - V priečinku školského roka sú ďalšie podpriečinky podľa typu udalosti (`prednasky`, `seminare`, `sutaze`, `olympiady`).
    - Tie obsahujú konkrétne priečinky pre jednotlivé akcie (pokiaľ majú tieto akcie viac udalostí, napríklad viac kôl súťaže).
      Inak sú v nich priamo súbory udalostí.

Priečinky školských rokov sa používajú na kontrolu správneho dátumu udalosti (pozri viac v časti Kontrola súborov).
Inak Kalendáru v podstate vôbec nezáleží na tom, kde sa tento súbor udalosti nachádza.
Ale nám na tom záleží, aby sme mali dáta prehľadné.

### Súbory

YAML súbor udalosti má presne definovanú štruktúru, ktorú nájdeš [tu](https://github.com/kockatykalendar/data/blob/master/schemas/event.schema.json).
Užitočnejší ale pre teba bude [príklad, ako sa používa](https://github.com/kockatykalendar/data/blob/master/example.yml).

Najjednoduchší spôsob, ako vyrobiť novú udalosť, je skopírovať si príklad (`example.yml`) alebo udalosť z minulého roka a zmeniť relevantné údaje.

### Obsah súborov

Niekoľko užitočných konvencií, ktoré sa oplatí dodrživať, aby jednotlivé udalosti vyzerali v Kalendári konzistentne.

#### Názvy

Pokiaľ sa jedná o kolo konkrétnej súťaže / semináru, názov udalosti by mal obsahovať aj názov súťaže / semináru, nie len dané kolo.
Táto informácia totiž nie je inak dostatočne viditeľná.
Takže ideálne `KSP - prvé kolo zimnej časti`, nie iba ~~`Prvé kolo zimnej časti`~~.

Skratky môžu byť aj rozpísané, ale rozpísaním sa znižuje prehľadnosť danej udalosti.
Pokiaľ sú teda skratky dobre známe, pravdepodobne sa to robiť neoplatí.

Názov má byť stručný.
Pokiaľ má daná súťaž viac podobných udalostí, chcú byť v názve iba skutočnosti, ktoré sa medzi nimi líšia (napríklad číslo kola),
na všetko ostatné je určený popis.

#### Popisy

Popisy jednotlivých udalostí majú maximálnu dĺžku cca 250 znakov.
To najmä preto, aby na stránke nezaberali priveľa miesta.

Nemal by to však byť problém -- popis má iba vysvetľovať, čo je dána udalosť zač, ak to nie je jasné z nadpisu, prípadne jej robiť reklamu niečim zaujímavým.

Popis nemusí (ba priam nemá) obsahovať:
- Kde a kedy udalosť prebieha -- sú na to samostatné vlastnosti, ktoré sa zobrazia pod ním
- Pre koho je udalosť určená (z hľadiska ročníku) -- je na to samostatná vlastnosť
	- Informácia, že udalosť má aj "open" kategóriu bez vekového obmedzenia, sa naopak do popisu hodí
- Akej oblasti (vedy) sa udalosť týka -- je na to samostatná vlastnosť
	- Pokiaľ je to oblasť, ktorú nemáme zahrnutú vo výbere, teda `other`, tak sa naopak táto informácia do popisu hodí 
 	- Pokiaľ je súťaž multiodborová, môže byť táto informácia v popise relevantná
- Pravidlá súťaže, podrobný priebeh -- na to existuje odkaz na stránku súťaže, kde si vie pravidlá ktokoľvek nájsť

Ak si s popisom nevieš rady, kľudne nenapíš nič, alebo proste napíš niečo, a nejaký data-manager to upraví alebo ti povie, čo zmeniť.

Popisy sa momentálne nezobrazujú na mobile. Plán do budúcnosti je spraviť ich v mobilnom rozhraní rozkliknuteľné.

#### Miesta

Vlastnosť miesta je nepovinná.

Pokiaľ udalosť prebieha online, konvencia je napísať `online` (s malým písmenom).
Pokiaľ miesto nie je známe alebo nie je dôležité, vlastnosť sa vynecháva
(takže prosím žiadne `TODO`, `TBA`, `TBD`, `TO DO`, `???` a podobne -- DO zo slova TODO už nikdy nikto nespraví).

#### Dátumy

Štandardne musí mať každá udalosť začiatok, voliteľne môže mať aj koniec.
Pokiaľ koniec nemá, považuje sa za jednodňovú, teda končiacu v rovnaký deň ako sa začína.

Pokiaľ ide napríklad o kolo korešpondenčého semináru, zvykne sa uvádzať len termín jeho konca
(pričom je ale z technických príčin vyplnená iba vlastnosť `start`).
Hlavný dôvod je pravdepodobne taký, že začiatky často nie sú jednoznačne určené / nestíhajú sa / nie sú až tak dôležité.

Nevýhoda tohto prístupu ale je, že kalendár nezobrazuje kolo ako prebiehajúcu udalosť.
Ak chceš teda maximalizovať viditeľnosť nejakej prebiehajúcej súťaže, odporúčame nastaviť aj jej začiatok.
Vlastne to odporúčame za každých okolností.

#### Notifikácie

V príklade schémy je vlastnosť `notifications`. Janči momentálne netuší, či funguje, či niekedy fungovala, ani ako presne.
Je ale v pláne ju nejakým spôsobom implementovať, takže ju môžeš použiť podľa príkladu, kopírovať do ďalších rokov, a v budúcnosti by mala fungovať.

### Nedokončené / skryté súbory

Občas sa oplatí vyrobiť si naraz viac súborov, než chceš nahrať --
napríklad pokiaľ vieš, že súťaž má počas roka 5 sérií, ale len prvá má známe termíny.
Vtedy si môžeš vyrobiť všetky súbory s popismi, ale niektoré z nich schovať.

Robí sa to jednoducho tak, že zmažeš z názvu súboru príponu `.yml`.
Vďaka tomu ho bude git ignorovať (zostane iba u teba na počítači, ako každý súbor v priečinku `data` bez prípony)
a pri kontrole súborov sa nebude kontrolovať (takže v ňom môžu napríklad chýbať dátumy).

### Kontrola súborov (a buildovanie)

Kontrola slúži na automatické hľadanie chýb ako nesprávny formát súboru, jeho jednotlivých vlastností (napríklad dátumu),
alebo toho, že udalosť má dátum mimo školského roka, v ktorom je uložená, obsahuje nedefinované miesto, a podobne.

Kontrola sa spúšťa automaticky pri každom commite, takže ju robiť v princípe nemusíš.
Výsledok kontroly sa ukazuje na githube priamo v pull-requeste, k detailom sa dá dostať postupným klikaním na krížiky / fajky.

#### Kontrola lokálne

Na spustenie potrebuješ `Python 3`, `pip` (súčasť Pythonu) a knižnice, ktoré nainštaluješ pomocou `pip install -r requirements.txt`.
Pokiaľ používaš Python aj na niečo iné, odporúčame sa naučiť používať `venv`
([virtuálne prostredie](https://rcd.ucsb.edu/sites/default/files/2023-12/DLS-202312-Venv.pdf)).

Na kontrolu sa používa script `build.py`, ktorý sa okrem toho používa aj na buildovanie súborov, ktoré sa priamo zverejňujú.
**To robiť nemusíš**. Priečinok `build`, ktorý pri tom vzniká, môžeš u seba kľudne zmazať.

Na kontrolu, či sú YML súbory správne, stačí spustiť `python build.py --dry --now`.
- `--dry` znamená, že sa nič nebuilduje (teda nevznikne priečinok `build`)
- `--now` znamená, že sa kontrolujú len zmeny z aktuálneho školského roka
- `build.py` má zopár ďalších nastavení súvisiacich s testovaním, tie si môžeš pozrieť pomocou `python build.py -h`.

Väčšinou dostaneš na výstupe výpis s pár upozorneniami, ktoré sa týkajú iných akcií (a možno aj akcie, ktorú pridávaš).
Na konci bude potom buď riadok s `Validation successful...`, ak je všetko v poriadku,
alebo výpis chýb, ktoré treba opraviť. 

## Pridávanie organizátorov

Každý organizátor má svoj `.yml` súbor v priečinku `organizers`.
Kalendáru nezáleží, kde sa tento súbor v priečinku nachádza, ale priečinok zatiaľ nie je konkrétnejšie štruktúrovaný.
V podpriečinku `logos` sú uložené logá, na ktoré je zo súboru uvedený relatívny odkaz v atribúte `icon`.

Dĺžka názvu organizátora je limitovaná na 32 znakov, aby sa rozumne zmestil na jeden riadok aj pri zobrazení na mobile.
Ak je to problém, sťažuj sa, na niečo spolu prídeme.

## VSCode

Ak používaš Visual Studio Code na úpravu dát, odporúčame si nainštalovať
[YAML extension](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml).
Potom v nastaveniach projektu (`.vscode/settings.json`) môžeš zadefinovať,
že chceš používať schému a aktivuješ si tak autocomplete:

```json
{
    "yaml.schemas": {
        "./schemas/event.schema.json": ["/data/*.yaml", "/data/*.yml"],
        "./schemas/organizers.schema.json": ["/organizers/*.yaml", "/organizers/*.yml"],
    }
}
```

## README

Ak nájdeš v tomto texte chybu alebo niečo, čo nie je dostatočne vysvetlené, neváhaj upraviť súbor `README.md` a otvoriť si pull-request.

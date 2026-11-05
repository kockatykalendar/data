# Changelog

Všetky podstatné zmeny tohto projektu by mali byť zaznamenané v tomto súbore.

Formát changelogu založený na [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
používame [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.1.0 - 2026-11-05
### Added
- Nové vedné obory v `sciences`: `any` (akcia pre všetky obory), `bio` a `chem`.
- Pridané nepovinné `country_override` pri eventoch na prepísanie krajiny organizátorov (`sk`, `cz` alebo `international`).
- Pridaná krajina organizátora `country` s hodnotami `sk`, `cz` a `international`.

### Changed
- `places` pri eventoch už nie je povinné; namiesto zástupných hodnôt (napr. `TBA`) ho treba vynechať.
- Krajina organizátora `country` je povinná (pôvodne nepovinná s predvolenou hodnotou `sk`).
- Názov organizátora `name` môže mať najviac 32 znakov (kvôli zobrazeniu na mobile).
- Popis flagu `volatile` už nespomína COVID-19, označuje udalosti, ktoré sa nemusia uskutočniť z budúcich príčin.

## 0.0.6 - 2022-07-17
### Added
- Pridané `color` pri organizátoroch na zmenu predvolenej farby ich udalostí.

## 0.0.5 - 2022-05-24
### Changed
- Pri organizátoroch vyžadujeme okrem `name` aj `web` a `icon`.
- Typ organizátora `type` má predvolenú hodnotu `other`.

## 0.0.4 - 2022-02-28
### Added
- Pridaný flag `cancelled` na označenie zrušených udalostí.
- Pridaná schéma pre organizátorov

### Changed
- Pri eventoch vyžadujeme `contestants.min` aj `contestants.max`, pričom obe môžu byť `null`. Issue #26.
- Pri eventoch vyžadujeme v zozname `organizers` boli iba validny organizátori
- Prechod na najnovší draft json schema (2020-12)

## 0.0.3 - 2020-11-03
### Added
- Pridané `color` na zmenu farby udalosti v kalendári.
- Pridaný flag `volatile`, ktorý označuje udalosti, ktorých organizácia môže byť ovplyvnená COVID-19 situáciou.

### Changed
- Dĺžka `short-info` sa už neoveruje pomocou regexov, ale pomocou `maxLength`.

## 0.0.2 - 2020-10-12
### Added
- Pridané pole `short-info` určené pre krátky popis eventu.

## 0.0.1 - 2020-05-19
### Added
- Základný návrh schémy.
- Základný parser založený na `fastjsonschema`.

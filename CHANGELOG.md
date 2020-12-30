# Changelog

Všetky podstatné zmeny tohto projektu sú zaznamenané v tomto súbore.

Formát changelogu založený na [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
používame [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased
### Added
- Pridaný flag `cancelled` na označenie zrušených udalostí.

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

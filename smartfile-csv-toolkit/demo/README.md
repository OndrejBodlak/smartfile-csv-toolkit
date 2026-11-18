# SmartFile – ukázka čištění produktových CSV dat

**Praktická ukázka automatizovaného čištění a sjednocování produktových dat pro e-shopy.**

Tato demonstrace používá 100 fiktivních produktových záznamů. Ukazuje, jak lze z neuspořádaného CSV souboru připravit přehlednější a jednotně formátovaný výstup.

> Veškerá produktová data v této ukázce jsou smyšlená. Nejde o zpracování skutečné zákaznické zakázky.

## Co ukázka řeší

Vstupní soubor `messy_products.csv` záměrně obsahuje několik běžných problémů:

- duplicitní SKU,
- nekonzistentní zápis kategorií,
- ceny v různých formátech,
- přebytečné mezery,
- chybějící názvy produktů,
- chybějící skladové hodnoty.

## Co se při zpracování provede

Skript `clean_products.py`:

1. Načte produktová data ze souboru CSV.
2. Očistí mezery a sjednotí vybrané textové hodnoty.
3. Převede platné ceny na formát se dvěma desetinnými místy.
4. Sjednotí zápis kategorií.
5. Odstraní duplicitní SKU a ponechá jejich první výskyt.
6. Zaznamená chybějící nebo neplatné hodnoty.
7. Vytvoří vyčištěný CSV soubor a strojově čitelný report.

Pravidla čištění jsou záměrně jednoduchá a jsou určena pro tuto demonstrační strukturu dat. U skutečných dat je potřeba předem potvrdit například pravidla pro identifikaci duplicit a zacházení s neúplnými produkty.

## Výsledek demonstračního běhu

| Ukazatel | Výsledek |
|---|---:|
| Načtené produkty | 100 |
| Exportované produkty | 96 |
| Odstraněné duplicitní SKU | 4 |
| Chybějící názvy | 3 |
| Chybějící skladové hodnoty | 7 |
| Neplatné nebo chybějící ceny | 0 |
| Podíl exportovaných záznamů | 96 % |

### Provedené úpravy

| Úprava | Počet |
|---|---:|
| Normalizované ceny | 96 |
| Normalizované kategorie | 44 |
| Odstraněné přebytečné mezery | 65 |

Počty výše odpovídají aktuálnímu demonstračnímu datasetu. Nejde o garantovaný výsledek pro libovolný zákaznický soubor.

## Výstupní soubory

Po spuštění vzniknou:

- `clean_products.csv` – vyčištěný produktový katalog.
- `cleanup_report.json` – statistiky ve strojově čitelné podobě.
- `cleanup_report.html` – přehledný report s výsledky zpracování.

HTML report zobrazuje počet načtených a exportovaných záznamů, provedené úpravy a kontrolu kvality dat.

## Spuštění ukázky

Požadavky: Python 3.11 nebo novější. Ukázka používá pouze standardní knihovnu Pythonu.

Z kořenové složky projektu spusť v PowerShellu:

```powershell
python .\demo\generate_demo.py
python .\demo\clean_products.py
python .\demo\generate_report.py
Start-Process .\demo\cleanup_report.html
```

## Automatické testy

Spusť testovací sadu příkazem:

```powershell
python -m unittest discover -s .\demo -p "test_*.py" -v
```

Aktuální sada obsahuje 11 testů základního zpracování, formátování cen, duplicit a vybraných hraničních případů.

## Struktura složky

```text
demo/
├── generate_demo.py
├── clean_products.py
├── generate_report.py
├── test_demo.py
├── test_edge_cases.py
├── test_cleaning_rules.py
├── messy_products.csv
├── clean_products.csv
├── cleanup_report.json
└── cleanup_report.html
```

Generované CSV a reporty se vytvářejí při spuštění skriptů. Pokud je v repozitáři nenajdeš, vygeneruj je podle postupu výše.

## Zpracování zákaznických dat

Stejný princip lze přizpůsobit konkrétnímu formátu a požadavkům e-shopu, například pro:

- čištění a sjednocení produktových katalogů,
- odstraňování duplicit podle dohodnutého identifikátoru,
- spojování souborů od více dodavatelů,
- úpravy cen, kategorií a dalších sloupců,
- automatizaci opakovaného zpracování CSV.

Před úpravou skutečných dat je potřeba odsouhlasit pravidla čištění a ověřit výsledek na kopii nebo anonymizovaném vzorku.

---

**SmartFile CSV Toolkit – méně ruční práce, čistší produktová data.**

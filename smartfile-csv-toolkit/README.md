# SmartFile CSV Toolkit

A small Python command-line tool for cleaning, merging and inspecting CSV files.
It uses only Python's standard library. Files are processed locally; nothing is uploaded.

## Requirements
- Python 3.10 or newer
- No third-party packages

## Quick start (Windows)
Open Command Prompt or PowerShell in this folder:

```powershell
python smartfile.py --help
python smartfile.py clean samples/orders_january.csv --output cleaned.csv --dedupe
python smartfile.py merge samples/orders_january.csv samples/orders_february.csv --output all_orders.csv --dedupe
python smartfile.py stats samples/orders_january.csv
```

## Commands
- `clean INPUT -o OUTPUT [--dedupe]` trims whitespace, skips completely blank rows and optionally removes identical rows.
- `merge INPUT... -o OUTPUT [--dedupe] [--delimiter ,|;|TAB]` merges files and keeps the union of their columns.
- `stats INPUT` prints row/column counts and non-empty values per column.

## Tests
```powershell
python -m unittest discover -s tests -v
```

## Limitations
- CSV files only (not `.xlsx` workbooks).
- Duplicate removal compares all output columns.
- Always keep a backup of important source files.
- Test with a copy of customer data before using it in a real workflow.

## Portfolio description
SmartFile is a local CSV utility built with Python's `csv`, `argparse` and `pathlib` modules.
It demonstrates file handling, input validation, error handling, data cleaning, merging and automated tests.

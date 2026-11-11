# SmartFile — CSV Toolkit

**A lightweight Windows desktop app for cleaning, merging and inspecting CSV files.**

SmartFile helps combine CSV exports, remove duplicate rows and preview the result before exporting. Files are processed locally on your computer.

## Preview

The application has a dark desktop interface with:
- CSV import using a file picker or drag and drop
- Merge multiple files, including files with different columns
- Remove duplicate rows
- Preview up to 500 rows
- Row, column and duplicate counters
- CSV export using a semicolon delimiter by default for Czech Excel regional settings

## Download

A packaged Windows build will be published in **GitHub Releases** after the release is verified. Until then, use the source instructions below.

## Run from source (Windows)

1. Install Python 3.11 or newer.
2. Clone or download this repository.
3. Open PowerShell in the `smartfile-csv-toolkit` folder.
4. Install dependencies and start the app:

```powershell
python -m pip install -r requirements.txt
python smartfile_release.py
```

## Build the Windows app

Run `build_windows.bat` from the project folder. The generated one-folder application will be placed in `dist\\SmartFile\\`.

**Important:** Share the complete `dist\\SmartFile\\` folder (or a ZIP of it), not only `SmartFile.exe`, because the `_internal` folder contains bundled runtime files.

## Project structure

```text
smartfile-csv-toolkit/
├── smartfile.py             # CSV processing functions and CLI
├── smartfile_release.py     # Desktop GUI
├── smartfile.ico            # Windows application icon
├── build_windows.bat        # Windows build script
├── requirements.txt
├── samples/                 # Example CSV input files
└── tests/                   # Automated tests
```

## Privacy

SmartFile processes files locally. It does not upload CSV contents to a server.

## Limitations

- CSV files only; Excel workbooks (`.xlsx`) are not supported.
- The preview is limited to 500 rows; export includes the full result.
- Duplicate detection compares values across all output columns.
- Always test with copies of important files before using the app in a business-critical workflow.

## Development

Run the automated tests:

```powershell
python -m unittest discover -s tests -v
```

See [CHANGELOG.md](smartfile-csv-toolkit/CHANGELOG.md) for release notes.

## License

No open-source license has been added yet. Until a license is selected, standard copyright restrictions apply.

# SmartFile — CSV Toolkit

**A lightweight Windows desktop application for cleaning, merging and managing CSV files.**

SmartFile makes working with CSV files simple. Import multiple files, merge their data, remove duplicate rows and export the result in seconds.

## Download

**[Download SmartFile 1.0.0 for Windows](https://github.com/OndrejBodlak/smartfile-csv-toolkit/releases/latest)**

1. Download the ZIP archive.
2. Extract the ZIP file.
3. Open the extracted folder.
4. Run `SmartFile.exe`.

Windows 10 / Windows 11.

## Features

- Drag & drop CSV file import
- Merge multiple CSV files
- Support for different column structures
- Automatic duplicate removal
- Data preview (up to 500 rows)
- Row and column statistics
- CSV export compatible with Czech Excel settings
- Modern dark user interface

## Screenshots

*Application screenshots coming soon.*

## Privacy

SmartFile processes files locally on your computer. Your CSV data is not uploaded to external servers.

## Built With

- Python 3.11+
- CustomTkinter
- tkinterdnd2
- PyInstaller

## Run From Source

```powershell
python -m pip install -r requirements.txt
python smartfile_release.py
```

## Build

Run `build_windows.bat` to create the Windows application in `dist/SmartFile/`.

Share the complete folder, including `_internal`, rather than the EXE alone.

## Limitations

- CSV files only; `.xlsx` workbooks are not supported.
- Preview is limited to 500 rows.
- Duplicate detection compares values across all output columns.

## Project Structure

```text
smartfile-csv-toolkit/
├── smartfile.py
├── smartfile_release.py
├── smartfile.ico
├── requirements.txt
├── build_windows.bat
├── samples/
└── tests/
```

## Tests

```powershell
python -m unittest discover -s tests -v
```

## Release History

See [CHANGELOG.md](smartfile-csv-toolkit/CHANGELOG.md).

## License

No open-source license has been added yet.

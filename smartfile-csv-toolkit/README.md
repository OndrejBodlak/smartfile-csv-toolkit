# SmartFile 1.0

A lightweight Windows desktop tool for cleaning, merging, previewing and exporting CSV files. Files are processed locally on your computer.

## Features

- Import multiple CSV files using the file picker or drag and drop
- Merge files with different column sets
- Remove duplicate rows
- Preview up to 500 rows in the desktop interface
- View row, column and removed-duplicate counts
- Export CSV using a semicolon delimiter by default for compatibility with many Czech Excel regional settings
- Supports UTF-8 BOM and common delimiters (comma, semicolon, tab and pipe) when reading input files

## Requirements for running from source

- Python 3.11 or newer
- Windows recommended for the packaged build

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run the application:

```powershell
python smartfile_release.py
```

## Build the Windows application

1. Keep `smartfile.ico`, `smartfile.py`, `smartfile_release.py`, `requirements.txt` and `build_windows.bat` in the same project folder.
2. Double-click `build_windows.bat`.
3. When the build finishes, launch `dist\\SmartFile\\SmartFile.exe`.

The build creates a one-folder distribution. Share the entire `dist\\SmartFile` folder (or zip that folder), not only the EXE, because `_internal` contains bundled runtime files.

## Project structure

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

## Privacy

CSV files are read and processed locally. SmartFile does not upload your data to a server.

## Limitations

- The preview displays at most 500 rows; the exported file contains all processed rows.
- Duplicate detection compares the values across all output columns.
- This is an early release. Test the packaged application with copies of important files before relying on it for business-critical data.

## License

Choose and add a license before accepting outside contributions or distributing modified versions.

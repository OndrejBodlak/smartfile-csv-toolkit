# SmartFile source

See the [main repository README](../README.md) for the project overview, features, setup, build instructions and limitations.

## Run locally

```powershell
python -m pip install -r requirements.txt
python smartfile_release.py
```

## Build for Windows

Run `build_windows.bat`. The packaged application is created in `dist\\SmartFile\\`. Distribute the complete folder, including `_internal`, or ZIP the folder.

## Tests

```powershell
python -m unittest discover -s tests -v
```

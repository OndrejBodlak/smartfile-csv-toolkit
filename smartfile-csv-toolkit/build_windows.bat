@echo off
setlocal
cd /d "%~dp0"

echo ==========================================
echo          SmartFile 1.0 Release Builder
echo ==========================================
echo.

python -m pip install -r requirements.txt
if errorlevel 1 goto error

echo.
echo Building SmartFile 1.0...
python -m PyInstaller --noconfirm --clean --windowed --name SmartFile --icon=smartfile.ico --add-data "smartfile.ico;." --collect-all customtkinter --collect-all tkinterdnd2 smartfile_release.py
if errorlevel 1 goto error

echo.
echo BUILD COMPLETE!
echo Your application is in dist\SmartFile\
echo Run dist\SmartFile\SmartFile.exe to test it.
echo.
pause
exit /b 0

:error
echo.
echo BUILD FAILED. Copy the error above and send it for troubleshooting.
pause
exit /b 1

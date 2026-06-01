@echo off
REM CB PMR Logbook - Build script pro Windows
REM ==========================================

echo.
echo 📦 Instaluji PyInstaller...
pip install -q pyinstaller

echo.
echo 📦 Instaluji zavislosti projektu...
pip install -q -r requirements.txt

echo.
echo 🏗️ Staví .exe soubor...
pyinstaller cb_pmr_logbook.spec --distpath ./dist --workpath ./build

if %errorlevel% equ 0 (
    echo.
    echo ✅ HOTOVO! Soubor byl úspešně vytvoren!
    echo 📍 Cesta: ./dist/CB_PMR_Logbook.exe
    echo.
    echo 📂 Strukturu vystupu muzes videt v adresari dist/
    pause
) else (
    echo.
    echo ❌ Chyba pri stavbe! Zkontroluj vypis vyse.
    pause
    exit /b 1
)

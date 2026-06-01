#!/bin/bash

# CB PMR Logbook - Build script pro vytvoření .exe souboru
# =========================================================

echo "📦 Instaluji PyInstaller..."
pip install -q pyinstaller

echo "📦 Instaluji závislosti projektu..."
pip install -q -r requirements.txt

echo "🏗️ Staví .exe soubor..."
pyinstaller cb_pmr_logbook.spec --distpath ./dist --workpath ./build

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ HOTOVO! Soubor byl úspěšně vytvořen!"
    echo "📍 Cesta: ./dist/CB_PMR_Logbook.exe"
    echo ""
    echo "📂 Struktura výstupního adresáře:"
    ls -la ./dist/
else
    echo "❌ Chyba při stavbě! Zkontroluj výstup výše."
    exit 1
fi

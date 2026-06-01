# 🏗️ Stavba .EXE souboru - CB PMR Logbook

Tento adresář obsahuje všechny potřebné soubory pro vytvoření spustitelného .exe souboru aplikace CB PMR Logbook.

## 📋 Předpoklady

- **Python 3.8+** (nainstalovaný a v PATH)
- **pip** (součást Python)
- **Přístup na internet** (pro stažení balíčků)

## 🚀 Jak stavit .exe

### Na Windows
```bash
build_exe.bat
```

### Na Linux/Mac
```bash
chmod +x build_exe.sh
./build_exe.sh
```

## 📁 Výstup

Po úspěšné stavbě bude výsledný .exe soubor v adresáři:
```
./dist/CB_PMR_Logbook.exe
```

Aplikace bude obsahovat:
- ✅ Zdrojový kód (`main.py`)
- ✅ README a dokumentaci
- ✅ Všechny potřebné Python knihovny
- ✅ Python runtime

## 🎛️ Obsah build procesů

### `cb_pmr_logbook.spec`
PyInstaller konfigurační soubor, který definuje:
- Vstupní soubor (`main.py`)
- Zabalované soubory (zdrojový kód, README, requirements)
- Skryté importy pro all knihovny
- Nastavení výstupu

### `build_exe.bat` (Windows)
Dávkový skript, který:
1. Instaluje PyInstaller
2. Instaluje závislosti z `requirements.txt`
3. Spouští PyInstaller se spec souborem
4. Zobrazí cestu k výslednému .exe

### `build_exe.sh` (Linux/Mac)
Bash skript - stejná funkce jako .bat, ale pro Unix systémy

## 🔧 Ruční stavba

Pokud chceš stavět přímo bez skriptů:

```bash
pip install pyinstaller
pip install -r requirements.txt
pyinstaller cb_pmr_logbook.spec
```

## 📦 Velikost výstupu

Výsledný .exe bude asi **100-150 MB** (zahrnuje Python runtime a všechny knihovny).

## ⚠️ Antivirus varování

Některé antivirové programy mohou PyInstaller .exe soubory falešně detekovat jako hrozby (false positive). Je to normální a není to vada aplikace.

## 🐛 Řešení problémů

**Problém:** `ModuleNotFoundError` při spuštění .exe
- **Řešení:** Ujisti se, že máš v `cb_pmr_logbook.spec` všechny potřebné `hiddenimports`

**Problém:** .exe se otevře a hned zavře
- **Řešení:** Spusť .exe z příkazové řádky, aby ses viděl chybovou zprávu:
  ```bash
  dist\CB_PMR_Logbook.exe
  ```

**Problém:** Map se v aplikaci nenačítají
- **Řešení:** Je potřeba internetové připojení pro stažení map dlaždiček

## 📄 Licencování

Distribuce tohoto .exe souboru podléhá licencím použitých knihoven:
- `customtkinter` - BSD License
- `tkintermapview` - MIT License
- `geopy` - MIT License

---

**Vytvořeno:** 2026  
**Poslední aktualizace:** 1. června 2026

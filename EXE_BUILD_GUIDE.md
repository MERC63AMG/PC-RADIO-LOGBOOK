# 🏗️ STAVBA .EXE SOUBORU - KOMPLETNÍ PRŮVODCE

## ⚠️ DŮLEŽITÉ: Tato aplikace se musí stavět na **Windows** systému

Z důvodu technických omezení PyInstalleru nelze stavět .exe soubory na Linuxu bez Wine/EXE emulátoru. Nejlepší řešení je stavět přímo na Windows.

---

## 🖥️ STAVBA NA WINDOWS

### Předpoklady
- ✅ Windows 10 nebo novější
- ✅ Python 3.8+ (https://www.python.org/downloads/)
  - **DŮLEŽITÉ:** Při instalaci zaškrtni "Add Python to PATH"
- ✅ Git (https://git-scm.com/download/win) - volitelně

### Krok 1️⃣: Klonování/stažení repozitáře

```bash
git clone https://github.com/MERC63AMG/PC-RADIO-LOGBOOK.git
cd PC-RADIO-LOGBOOK
```

Nebo si stáhni ZIP a rozbal ho.

### Krok 2️⃣: Otevření příkazové řádky v projektu

```bash
# Naviguj do složky projektu a otevři CMD
cd C:\cesta\k\PC-RADIO-LOGBOOK
```

### Krok 3️⃣: Spuštění build skriptu

```bash
build_exe.bat
```

Skript automaticky:
1. ✅ Instaluje PyInstaller
2. ✅ Instaluje všechny závislosti
3. ✅ Staví .exe soubor
4. ✅ Vytvoří složku `dist/` s finálním souborem

### Krok 4️⃣: Nalezení výsledného .exe

```
dist/CB_PMR_Logbook.exe
```

Tento soubor lze spustit na jakémkoli Windows počítači bez instalace Pythonu.

---

## 🐧 STAVBA NA LINUXU / MAC (pokročilé)

Na Unixových systémech doporučuji jiný přístup - vytvoření distribučního balíčku:

### Alternativa 1: Vytvoření distribučního balíčku (Wheel)

```bash
pip install wheel
python setup.py bdist_wheel
```

Výstup: `dist/*.whl` - lze instalovat kdekoliv kde je Python

### Alternativa 2: Přenosná Python aplikace (Zipapp)

```bash
pip install pyzzer
python -m pyzzer main.py -o CB_PMR_Logbook.pyz
```

### Alternativa 3: Docker kontejner

Pro distribuce Linux aplikací lze použít Docker:

```bash
docker build -t cb-pmr-logbook .
docker run -d cb-pmr-logbook
```

---

## 📋 OBSAH BUILD SOUBORŮ

| Soubor | Popis |
|--------|-------|
| `cb_pmr_logbook.spec` | PyInstaller konfigurační soubor |
| `build_exe.bat` | Windows build skript |
| `build_exe.sh` | Linux/Mac build skript |
| `setup.py` | Python setuptools konfigurační soubor |
| `BUILD_INSTRUCTIONS.md` | Tento soubor |

---

## 🔧 MANUÁLNÍ STAVBA (Pokročilé)

Pokud skript selže, můžeš stavět ručně:

```bash
# Instalace PyInstalleru
pip install pyinstaller

# Instalace závislostí
pip install -r requirements.txt

# Stavba (z jednoho souboru)
pyinstaller --onefile --windowed --add-data="main.py:." --add-data="README.md:." --add-data="requirements.txt:." --hidden-import=customtkinter --hidden-import=tkintermapview --hidden-import=geopy main.py

# Nebo se spec souborem
pyinstaller cb_pmr_logbook.spec
```

---

## 📦 VÝSLEDNÝ SOUBOR

### Velikost
- ~100-150 MB (obsahuje Python runtime a všechny knihovny)

### Složení
- `CB_PMR_Logbook.exe` - Spustitelný soubor
- Vložené knihovny:
  - customtkinter (GUI)
  - tkintermapview (Mapa)
  - geopy (Vzdálenosti)
  - Python 3.x runtime

### Spuštění
```bash
dist\CB_PMR_Logbook.exe
```

Nebo jednoduše dvaklikem na soubor.

---

## 🐛 ŘEŠENÍ PROBLÉMŮ

### ❌ "ModuleNotFoundError" při spuštění .exe

**Řešení:** Přidej modul do `hiddenimports` v `cb_pmr_logbook.spec`:

```python
hiddenimports=['customtkinter', 'tkintermapview', 'geopy', 'tvoj_modul'],
```

### ❌ "Python was built without shared library" na Linuxu

**Řešení:** Staví na Windows nebo použij Alternativu 1/2 výše.

### ❌ .exe se otevře a hned zavře

**Řešení:** Spusť z příkazové řádky:
```bash
dist\CB_PMR_Logbook.exe
```

Aby ses viděl chybovou zprávu.

### ❌ Mapa se nenačítá v .exe

**Řešení:** Je potřeba internetové připojení pro stažení map dlaždiček z OpenStreetMap/CartoDB.

---

## 🔐 BEZPEČNOST & ANTIVIRUS

Některé antivirové programy mohou PyInstaller .exe soubory detekovat jako hrozby - je to falešný poplach (false positive).

Pokud chceš zdrojový kód ověřit:
1. Zdrojový kód je v `main.py` - **otevřený a čitelný**
2. Všechny závislosti jsou z PyPI - veřejné a ověřené
3. Aplikace **NESPOUŠTÍ** žádné síťové komunikace mimo stažení map

---

## 📄 LICENCOVÁNÍ

Distribuce tohoto .exe souboru podléhá licencím:
- ✅ **customtkinter** - BSD License
- ✅ **tkintermapview** - MIT License
- ✅ **geopy** - MIT License
- ✅ **Python** - PSF License

---

## 📝 DALŠÍ KROKY

1. **Distribuce:**
   - Sdílej `dist/CB_PMR_Logbook.exe`
   - Nebo vytvoř instalátor pomocí NSIS/Inno Setup

2. **Aktualizace:**
   - Když upravíš kód, znovu spusť build skript
   - Vygeneruj novou verzi .exe

3. **Verzování:**
   - Aktualizuj verzi v `setup.py` (line 9)
   - Renomuj .exe: `CB_PMR_Logbook_v1.0.exe`

---

**Poslední aktualizace:** 1. června 2026  
**Vytvořeno pro:** CB PMR Logbook aplikaci

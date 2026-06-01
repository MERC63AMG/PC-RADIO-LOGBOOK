# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file pro CB PMR Logbook

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('main.py', '.'), ('README.md', '.'), ('requirements.txt', '.')],
    hiddenimports=['customtkinter', 'tkintermapview', 'geopy', 'geopy.distance', 'PIL', 'PIL.Image'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CB_PMR_Logbook',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

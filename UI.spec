# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import copy_metadata

a = Analysis(
    ['UI.py','sbc_bootstrapping\\sources.json','sbc\\encoding_problem\\deep_encoding.py','sbc\\encoding_problem\\encodings.json','sbc\\essential_files\\essentials.py','sbc\\essential_files\\string_mergers.py','sbc\\hasher\\aes256.py','sbc\\base.py','sbc\\operation_logger.py','sbc\\__init__.py','sbc_bootstrapping\\__init__.py','sbc_bootstrapping\\request_.py'],
    pathex=[],
    binaries=[],
    datas = copy_metadata('imageio') + copy_metadata('imageio-ffmpeg'),
    hiddenimports=['PIL'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=False,
    name='SBC executable v3',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    icon='icon.ico',
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SBC version 1.1',
)

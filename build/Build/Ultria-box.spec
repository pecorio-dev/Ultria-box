# -*- mode: python ; coding: utf-8 -*-
import os

_ROOT = os.path.normpath(os.path.join(SPECPATH, '..', '..'))
_ICON = os.path.join(_ROOT, 'Config', 'icon-win-claude.ico')

a = Analysis(
    [os.path.join(_ROOT, 'Ultria.py')],
    pathex=[_ROOT],
    binaries=[],
    datas=[
        (os.path.join(_ROOT, 'Config', 'Menu.txt'), 'Config'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Ultria-box',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=_ICON if os.path.isfile(_ICON) else None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='Ultria-box',
)

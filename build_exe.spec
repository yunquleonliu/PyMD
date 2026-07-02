# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

import sys
import os

# Get Python DLL path
python_dll = os.path.join(sys.base_prefix, 'python313.dll')

a = Analysis(
    ['src\\pymd_editor\\main.py'],
    pathex=[],
    binaries=[
        (python_dll, '.'),  # Include python313.dll in root
    ],
    datas=[
        ('src\\pymd_editor\\*.py', 'pymd_editor'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.QtWebEngineWidgets',
        'PyQt6.QtWebEngineCore',
        'PyQt6.QtWebChannel',
        'markdown2',
        'docx',
        'httpx',
        'lxml',
        'lxml.etree',
        'lxml._elementpath',
        'lxml.html',
        'lxml.sax',
        'lxml.objectify',
        'fitz',
        'pdf2docx',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PyMDEditor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 如果有图标文件，可以指定路径
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PyMDEditor',
)

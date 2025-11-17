# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules, collect_data_files
import os

# Adiciona todos os arquivos Python do src
datas = []
src_path = os.path.join(os.getcwd(), 'src')
for root, dirs, files in os.walk(src_path):
    for file in files:
        if file.endswith('.py'):
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, os.getcwd())
            dest_dir = os.path.dirname(relative_path)
            datas.append((file_path, dest_dir))

# Coleta todos os submódulos
hiddenimports = [
    'lexer', 'lexer.lexer', 'lexer.Token', 'lexer.Buffer', 'lexer.afn_to_afd',
    'lexer.AFD', 'lexer.AFD.AFDUnificado', 'lexer.AFD.AFDStringLiteral', 
    'lexer.AFD.AFDOperadoresLogicos', 'lexer.AFD.AFDOperadoresBooleanos',
    'lexer.AFD.AFDOperadoresAritmeticosRelacionais', 'lexer.AFD.AFDIdentificadores',
    'lexer.AFD.AFDDelimitadores', 'lexer.AFD.AFDDecimal', 'lexer.AFD.AFDComentariosLinha',
    'lexer.AFN', 'lexer.AFN.AFNCoralUnificado', 'lexer.AFN.AFNTransicoes',
    'parser', 'parser.parser', 'parser.ast_nodes', 'parser.first_follow',
    'interpreter', 'interpreter.interpreter',
    'utils', 'utils.utils',
]

a = Analysis(
    ['coral.py'],
    pathex=['src'],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
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
    a.binaries,
    a.datas,
    [],
    name='coral',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

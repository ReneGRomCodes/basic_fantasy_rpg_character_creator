# -*- mode: python -*-
import os

block_cipher = None

added_files = [
         ( 'gui/art/font', 'gui/art/font'),
         ( 'gui/art', 'gui/art'),
         ( 'save/characters.json', 'save')
         ]

a = Analysis(['main.py'],
             pathex=[os.path.abspath(".")],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
         cipher=block_cipher)

exe = EXE(pyz,
      a.scripts,
      a.binaries,
      a.zipfiles,
      a.datas,
      name='RPG_Character_Creator_v1.0.1_windows',
      debug=False,
      strip=False,
      upx=False,
      console=False
)

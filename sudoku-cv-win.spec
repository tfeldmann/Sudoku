# -*- mode: python -*-
a = Analysis(['.\\sudoku-cv.py'],
             pathex=['.'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='Sudoku-CV.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True , icon='.\\Resources\\Icon512.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='Sudoku-CV')

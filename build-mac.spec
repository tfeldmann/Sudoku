# -*- mode: python -*-
a = Analysis(['main.py'],
             pathex=['./'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts + [('O', '', 'OPTION')],
          exclude_binaries=True,
          name='Sudoku-CV',
          debug=False,
          strip=None,
          upx=True,
          console=False)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='Sudoku-CV')
app = BUNDLE(coll,
             name='Sudoku-CV.app',
             icon='Resources/Icon.icns')

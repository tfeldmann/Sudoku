# -*- mode: python -*-
a = Analysis(['sudoku-cv.py'],
             pathex=['./'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Sudoku-CV',
          debug=False,
          strip=None,
          upx=True,
          console=False )
app = BUNDLE(exe,
             name='Sudoku-CV.app',
             icon='Resources/Icon.icns')

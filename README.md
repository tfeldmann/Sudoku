<div align="center"><img src="Resources/Icon.png" alt="Sudoku-CV Icon"></div>

This program uses your webcam to detect and solve any given 9x9 sudoku.

It is written is Python and uses OpenCV for image processing and Tesseract for OCR. The sudoku is solved with the python-constraint library.

## Download
Coming soon.

- Mac OS X
- Windows

## Screenshots
Coming soon.

## Creating executables
First make sure you can run the program successfully with `python main.py`.
Then download *PyInstaller* and use one of the commands below:

```
Mac:
python -O pyinstaller.py -w build-mac.spec

Windows:
python -O pyinstaller.py -w build-win.spec
```


<div align="center"><img src="Resources/Icon.png" alt="Sudoku-CV Icon"></div>

Solve sudokus by showing them to your webcam.

This program is written in Python and uses OpenCV for image processing and Tesseract for OCR. The sudoku is solved using the python-constraint library.

## Screenshots
Coming soon.

## Download
Coming soon.

- Mac OS X
- Windows

## Running from source
This program is tested with `Python 2.7.5`, `OpenCV 2.4.7`,
`tesseract 3.02.02`, `numpy 1.8.0` and `python-tesseract`.

## Creating executables
First make sure you can run the program successfully with `python main.py`.
Then download *PyInstaller* and use one of the commands below:

```
Mac:
python -O pyinstaller.py -w build-mac.spec

Windows:
python -O pyinstaller.py -w build-win.spec
```

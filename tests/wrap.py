import os
import cv2
from tesserwrap import Tesseract, PageSegMode, tr
import ctypes


class Tesser(Tesseract):

    def __init__(self, datadir="", lang="equ"):
        print datadir
        super(Tesser, self).__init__(datadir=datadir, lang="eng")

    def set_cv2_image(self, image):
        tr.Tesserwrap_SetImage(
            self.handle,
            image.ctypes.data_as(ctypes.c_char_p),  # Image data
            len(image),      # size of buffer
            image.shape[0],  # Widthw
            image.shape[1])  # Height


# Open an image
im = cv2.imread("single_letter.png", cv2.IMREAD_GRAYSCALE)
cv2.imshow('im', im)

# Create a Tesseract object
thisdir = os.path.dirname(os.path.abspath(__file__))
print thisdir
tw = Tesser(datadir=thisdir+'/tessdata')
tw.set_variable("tessedit_char_whitelist", "0123456789")
tw.set_page_seg_mode(mode=PageSegMode.PSM_SINGLE_BLOCK)

# OCR the image and return a string
tw.set_cv2_image(im)
print tw.get_text()

cv2.waitKey(0)
cv2.destroyAllWindows()

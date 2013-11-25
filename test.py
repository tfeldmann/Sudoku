import cv2.cv as cv
import tesseract

api = tesseract.TessBaseAPI()
api.Init(".", "eng", tesseract.OEM_DEFAULT)
api.SetPageSegMode(tesseract.PSM_SINGLE_BLOCK)
api.SetVariable("tessedit_char_whitelist", "0123456789")
api.SetVariable("classify_enable_learning", "0")
api.SetVariable("classify_enable_adaptive_matcher", "0")

image = cv.LoadImage("5.png", cv.CV_LOAD_IMAGE_GRAYSCALE)

tesseract.SetCvImage(image, api)
text = api.GetUTF8Text()
conf = api.MeanTextConf()

print '"%s" Confidence: %s' % (text.strip(), conf)

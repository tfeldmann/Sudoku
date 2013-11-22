import cv2.cv as cv
import tesseract

api = tesseract.TessBaseAPI()
api.Init(".", "eng", tesseract.OEM_TESSERACT_ONLY)
api.SetVariable("tessedit_char_whitelist", "0123456789")
api.SetVariable("classify_enable_learning", "0")
api.SetVariable("classify_enable_adaptive_matcher", "0")

image = cv.LoadImage("7.png", cv.CV_LOAD_IMAGE_GRAYSCALE)

tesseract.SetCvImage(image, api)
text = api.GetUTF8Text()
conf = api.MeanTextConf()

print text

import cv2
import cv2.cv as cv
import tesseract


def iplimage_from_array(source):
    bitmap = cv.CreateImageHeader((source.shape[1], source.shape[0]),
                                  cv.IPL_DEPTH_8U, 1)
    cv.SetData(bitmap, source.tostring(),
               source.dtype.itemsize * source.shape[1])
    return bitmap


image = cv2.imread("../temp/5.png",  cv2.IMREAD_GRAYSCALE)
ipl = iplimage_from_array(image)

api = tesseract.TessBaseAPI()
api.Init(".", "eng", tesseract.OEM_DEFAULT)
api.SetPageSegMode(tesseract.PSM_SINGLE_BLOCK)
api.SetVariable("tessedit_char_whitelist", "0123456789")
api.SetVariable("classify_enable_learning", "0")
api.SetVariable("classify_enable_adaptive_matcher", "0")

tesseract.SetCvImage(ipl, api)

text = api.GetUTF8Text()
conf = api.MeanTextConf()
print '"%s" Confidence: %s' % (text.strip(), conf)

print image

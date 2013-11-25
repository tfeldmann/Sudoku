import cv2
import cv2.cv as cv
import matplotlib.pyplot as plt
import tesseract

api = tesseract.TessBaseAPI()
api.Init(".", "eng", tesseract.OEM_DEFAULT)
api.SetVariable("tessedit_char_whitelist", "0123456789")
api.SetVariable("classify_enable_learning", "0")
# api.SetVariable("classify_enable_adaptive_matcher", "0")
api.SetPageSegMode(tesseract.PSM_SINGLE_BLOCK)


def array2cv(a):
    dtype2depth = {
        'uint8':   cv.IPL_DEPTH_8U,
        'int8':    cv.IPL_DEPTH_8S,
        'uint16':  cv.IPL_DEPTH_16U,
        'int16':   cv.IPL_DEPTH_16S,
        'int32':   cv.IPL_DEPTH_32S,
        'float32': cv.IPL_DEPTH_32F,
        'float64': cv.IPL_DEPTH_64F,
    }
    try:
        nChannels = a.shape[2]
    except:
        nChannels = 1
    cv_im = cv.CreateImageHeader((a.shape[1], a.shape[0]),
                                 dtype2depth[str(a.dtype)], nChannels)
    cv.SetData(cv_im, a.tostring(), a.dtype.itemsize * nChannels * a.shape[1])
    return cv_im


def solve_sudoku_in_picture(filename):
    # read
    original = cv2.imread(filename, cv2.CV_LOAD_IMAGE_GRAYSCALE)

    # blur
    img = cv2.medianBlur(original, 3)

    img = cv2.adaptiveThreshold(
        img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    normed_size = cv2.resize(img, (450, 450))
    cv2.imshow('winname', normed_size)

    # all letters
    for y in range(0, 450, 50):
        for x in range(0, 450, 50):
            roi = normed_size[y + 5:y + 45, x + 5:x + 45]
            cv_roi = array2cv(roi)
            tesseract.SetCvImage(cv_roi, api)
            number = api.GetUTF8Text().strip()
            if number == '':
                print '_',
            else:
                print number,
        print('')

    cv2.waitKey(0)

    # histogram
    # hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    # plt.plot(hist)
    # plt.show()
    # binary

    # cv2.imshow('Treshold', img)
    # find contours
    # contours, hierarchy = cv2.findContours(
    #     img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # select biggest contour
    # biggest_contour = contours[0]
    # for c in contours:
    #     if cv2.contourArea(c) > cv2.contourArea(biggest_contour):
    #         biggest_contour = c
    # cv2.drawContours(original, [biggest_contour], 0, (255, 255, 255))
    # cv2.imshow('Biggest contour is not the sudoku', original)


if __name__ == '__main__':
    solve_sudoku_in_picture('sudoku-easy.png')

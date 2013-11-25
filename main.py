import cv2
import numpy as np


def solve_sudoku_in_picture(filename):
    # read
    original = cv2.imread(filename, cv2.CV_LOAD_IMAGE_GRAYSCALE)

    # blur
    img = cv2.medianBlur(original, 3)

    # threshold
    img = cv2.adaptiveThreshold(
        img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # invert
    img = cv2.bitwise_not(img)

    # find bigged contour
    contours, hierarchy = cv2.findContours(
        img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # select biggest contour
    biggest_contour = contours[0]
    for c in contours:
        if cv2.contourArea(c) > cv2.contourArea(biggest_contour):
            biggest_contour = c

    # create mask
    mask = np.zeros(img.shape, np.uint8)
    cv2.drawContours(mask, [biggest_contour], 0, 255, -1)

    # apply mask
    img = cv2.bitwise_and(original, mask)
    cv2.imshow('winname', img)

    # resize
    # normed_size = cv2.resize(img, (450, 450))
    # cv2.imshow('winname', normed_size)

    # ocr all letters
    # for y in range(0, 450, 50):
    #     for x in range(0, 450, 50):
    #         roi = normed_size[y + 5:y + 45, x + 5:x + 45]
    #         cv_roi = array2cv(roi)
    #         tesseract.SetCvImage(cv_roi, api)
    #         number = api.GetUTF8Text().strip()
    #         if number == '':
    #             print '_',
    #         else:
    #             print number,
    #     print('')

    # histogram
    # hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    # plt.plot(hist)
    # plt.show()
    # binary

if __name__ == '__main__':
    solve_sudoku_in_picture('sudoku.jpg')
    cv2.waitKey(0)
    cv2.destroyAllWindows()

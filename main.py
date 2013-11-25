import cv2
import numpy as np


def solve_sudoku_in_picture(filename):
    # read
    original = cv2.imread(filename, cv2.CV_LOAD_IMAGE_GRAYSCALE)

    # threshold
    img = cv2.adaptiveThreshold(original, 255,
                                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY, 11, 2)

    # median
    img = cv2.medianBlur(img, 3)

    # find contours
    inv = cv2.bitwise_not(img)
    contours, hierarchy = cv2.findContours(
        inv, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # select biggest contour
    biggest_contour = contours[0]
    for c in contours:
        if cv2.contourArea(c) > cv2.contourArea(biggest_contour):
            biggest_contour = c

    # create mask
    mask = np.zeros(img.shape, np.uint8)
    cv2.drawContours(mask, [biggest_contour], 0, 255, -1)
    mask_inv = cv2.bitwise_not(mask)

    # show only sudoku on white background
    img = cv2.bitwise_or(mask_inv, img)
    cv2.imshow('winname', img)


if __name__ == '__main__':
    solve_sudoku_in_picture('sudoku.jpg')
    cv2.waitKey(0)
    cv2.destroyAllWindows()

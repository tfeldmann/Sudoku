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

    # sobel x-axis
    sobel_x = cv2.Sobel(img, -1, 1, 0)
    kernel_x = np.array([[1]] * 9, dtype='uint8')

    # closing x-axis
    sobel_x = cv2.dilate(sobel_x, kernel_x)
    cv2.imshow('Sobel X', sobel_x)

    # sobel y-axis
    sobel_y = cv2.Sobel(img, -1, 0, 1)
    kernel_y = np.array([[[1]] * 9], dtype='uint8')

    # closing y-axis
    sobel_y = cv2.dilate(sobel_y, kernel_y)
    cv2.imshow('Sobel Y', sobel_y)

    cv2.imshow('winname', cv2.bitwise_and(sobel_y, sobel_x))

if __name__ == '__main__':
    solve_sudoku_in_picture('sudoku.jpg')
    cv2.waitKey(0)
    cv2.destroyAllWindows()

import cv2
import numpy as np


def cmp_height(x, y):
    _, _, _, hx = cv2.boundingRect(x)
    _, _, _, hy = cv2.boundingRect(y)
    return hy - hx


def cmp_width(x, y):
    _, _, wx, _ = cv2.boundingRect(x)
    _, _, wy, _ = cv2.boundingRect(y)
    return wy - wx


def solve_sudoku_in_picture(filename):
    # read
    original = cv2.imread(filename, cv2.CV_LOAD_IMAGE_GRAYSCALE)

    # threshold
    img = cv2.adaptiveThreshold(original, 255,
                                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY, 11, 2)

    img = cv2.medianBlur(img, 3)
    cv2.imshow('winname', img)

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

    # sobel x-axis
    sobel_x = cv2.Sobel(img, -1, 1, 0)
    kernel_x = np.array([[1]] * 15, dtype='uint8')

    # closing x-axis
    sobel_x = cv2.dilate(sobel_x, kernel_x)

    # generate mask for x
    contours, hierarchy = cv2.findContours(
        sobel_x, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    sorted_contours = sorted(contours, cmp=cmp_height)

    # fill biggest 10 on mask
    mask_x = np.zeros(img.shape, np.uint8)
    for c in sorted_contours[:10]:
        cv2.drawContours(mask_x, [c], 0, 255, -1)

    # sobel y-axis
    sobel_y = cv2.Sobel(img, -1, 0, 1)
    kernel_y = np.array([[[1]] * 15], dtype='uint8')

    # closing y-axis
    sobel_y = cv2.dilate(sobel_y, kernel_y)

    # generate mask for x
    contours, hierarchy = cv2.findContours(
        sobel_y, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    sorted_contours = sorted(contours, cmp=cmp_width)

    # fill biggest 10 on mask
    mask_y = np.zeros(img.shape, np.uint8)
    for c in sorted_contours[:10]:
        cv2.drawContours(mask_y, [c], 0, 255, -1)

    cv2.imshow('matrix', cv2.bitwise_and(mask_x, mask_y))

if __name__ == '__main__':
    solve_sudoku_in_picture('pics/sudoku.jpg')
    cv2.waitKey(0)
    cv2.destroyAllWindows()

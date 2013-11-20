import cv2
import matplotlib.pyplot as plt


def solve_sudoku_in_picture(filename):
    # read
    original = cv2.imread(filename, cv2.CV_LOAD_IMAGE_GRAYSCALE)

    # blur
    img = cv2.medianBlur(original, 3)

    # histogram
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    plt.plot(hist)
    plt.show()

    # binary
    img = cv2.adaptiveThreshold(
        img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2)
    cv2.imshow('Treshold', img)

    # find contours
    contours, hierarchy = cv2.findContours(
        img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # select biggest contour
    biggest_contour = contours[0]
    for c in contours:
        if cv2.contourArea(c) > cv2.contourArea(biggest_contour):
            biggest_contour = c

    cv2.drawContours(original, [biggest_contour], 0, (255, 255, 255))
    cv2.imshow('Biggest contour is not the sudoku', original)

if __name__ == '__main__':
    solve_sudoku_in_picture('sudoku-original.jpg')
    cv2.waitKey(0)

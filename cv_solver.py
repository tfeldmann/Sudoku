import cv2


def solve_sudoku_in_image(filename):
    original = cv2.imread(filename)
    cv2.imshow('Original', original)


if __name__ == '__main__':
    solve_sudoku_in_image('sudoku-original.jpg')
    cv2.waitKey(0)

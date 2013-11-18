import cv2


def solve_sudoku_in_picture(filename):
    original = cv2.imread(filename)
    cv2.imshow('Original', original)


if __name__ == '__main__':
    solve_sudoku_in_picture('sudoku-original.jpg')
    cv2.waitKey(0)

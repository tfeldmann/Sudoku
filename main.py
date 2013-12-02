import numpy as np
from cv2 import *
import tesseract
import sudoku


def draw_str(dst, (x, y), s):
    x, y = int(x), int(y)
    putText(dst, s, (x + 1, y + 1), FONT_HERSHEY_PLAIN,
            1.0, (0, 0, 0), thickness=2, lineType=CV_AA)
    putText(dst, s, (x, y), FONT_HERSHEY_PLAIN,
            1.0, (255, 255, 255), lineType=CV_AA)


def iplimage_from_array(source):
    bitmap = cv.CreateImageHeader((source.shape[1], source.shape[0]),
                                  cv.IPL_DEPTH_8U, 1)
    cv.SetData(bitmap, source.tostring(),
               source.dtype.itemsize * source.shape[1])
    return bitmap


def cmp_height(x, y):
    _, _, _, hx = boundingRect(x)
    _, _, _, hy = boundingRect(y)
    return hy - hx


def cmp_width(x, y):
    _, _, wx, _ = boundingRect(x)
    _, _, wy, _ = boundingRect(y)
    return wy - wx


def sort_rectangle_contour(a):
    '''
    Given a list of points that represent a quad, this function returns
    the list sorted from top to bottom, then left to right.
    '''
    w, h = a.shape
    sqrt_w = int(np.sqrt(w))
    # sort by y
    a = a[np.argsort(a[:, 1])]
    # put in groups
    a = np.reshape(a, (sqrt_w, sqrt_w, 2))
    # sort rows by x
    a = np.vstack([row[np.argsort(row[:, 0])] for row in a])
    # undo shape transformation
    a = np.reshape(a, (w, 1, 2))
    return a


def process(frame):

    #
    # preprocessing
    #
    gray = cvtColor(frame, COLOR_BGR2GRAY)
    binary = adaptiveThreshold(gray, 255,
                               ADAPTIVE_THRESH_GAUSSIAN_C,
                               THRESH_BINARY, 11, 2)
    blurred = medianBlur(binary, 3)
    contours, _ = findContours(bitwise_not(blurred), RETR_TREE,
                               CHAIN_APPROX_SIMPLE)

    #
    # try to find the sudoku
    #
    sudoku_area = 0
    sudoku_contour = None
    for cnt in contours:
        area = contourArea(cnt)
        x, y, w, h = boundingRect(cnt)
        if (0.7 < float(w) / h < 1.3     # aspect ratio
                and area > 150 * 150     # minimal area
                and area > sudoku_area   # biggest area on screen
                and area > .5 * w * h):  # fills bounding rect
            sudoku_area = area
            sudoku_contour = cnt

    #
    # separate sudoku from background
    #
    if sudoku_contour is not None:

        # first we make sure the found contour can be approximated by a quad
        perimeter = arcLength(sudoku_contour, True)
        approx = approxPolyDP(sudoku_contour, 0.1 * perimeter, True)

        if len(approx) == 4:
            # successfully approximated
            # we now transform the sudoku to a fixed size 450x450
            # plus 50 pixel border and remove the background
            mask = np.zeros(gray.shape, np.uint8)
            drawContours(mask, [sudoku_contour], 0, 255, -1)
            mask_inv = bitwise_not(mask)
            separated = bitwise_or(mask_inv, blurred)
            # imshow('separated', separated)

            square = np.float32([[50, 50], [500, 50], [50, 500], [500, 500]])
            approx = np.float32([i[0] for i in approx])  # conversion
            approx = sort_rectangle_contour(approx)

            m = getPerspectiveTransform(approx, square)
            transformed = warpPerspective(separated, m, (550, 550))
            imshow('transformed', transformed)

            #
            # get crossing points to determine grid convolution
            #

            #
            # vertical lines
            #

            # sobel x-axis
            sobel_x = Sobel(transformed, -1, 1, 0)
            kernel_x = np.array([[1]] * 20, dtype='uint8')

            # closing x-axis
            dilated_x = dilate(sobel_x, kernel_x)
            closed_x = erode(dilated_x, kernel_x)
            _, threshed_x = threshold(closed_x, 250, 255, THRESH_BINARY)

            # generate mask for x
            contours, _ = findContours(
                threshed_x, RETR_TREE, CHAIN_APPROX_SIMPLE)
            sorted_contours = sorted(contours, cmp=cmp_height)

            # fill biggest 10 on mask
            mask_x = np.zeros(transformed.shape, np.uint8)
            for c in sorted_contours[:10]:
                drawContours(mask_x, [c], 0, 255, -1)
            # imshow('mask_x', mask_x)

            #
            # horizontal lines
            #

            # sobel y-axis
            sobel_y = Sobel(transformed, -1, 0, 1)
            kernel_y = np.array([[[1]] * 20], dtype='uint8')

            # closing y-axis
            dilated_y = dilate(sobel_y, kernel_y)
            closed_y = erode(dilated_y, kernel_y)
            _, threshed_y = threshold(closed_y, 250, 255, THRESH_BINARY)

            # generate mask for y
            contours, _ = findContours(
                threshed_y, RETR_TREE, CHAIN_APPROX_SIMPLE)
            sorted_contours = sorted(contours, cmp=cmp_width)

            # fill biggest 10 on mask
            mask_y = np.zeros(transformed.shape, np.uint8)
            for c in sorted_contours[:10]:
                drawContours(mask_y, [c], 0, 255, -1)

            #
            # close the grid
            #
            dilated_ver = dilate(mask_x, kernel_x)
            dilated_hor = dilate(mask_y, kernel_y)
            grid = bitwise_or(dilated_hor, dilated_ver)
            crossing = bitwise_and(dilated_hor, dilated_ver)

            #
            # sort contours points
            #
            contours, _ = findContours(
                crossing, RETR_TREE, CHAIN_APPROX_SIMPLE)
            if len(contours) == 100:
                crossing_points = np.empty(shape=(100, 2))
                for n, cnt in enumerate(contours):
                    x, y, w, h = boundingRect(cnt)
                    cx, cy = (x + .5 * w, y + .5 * h)
                    crossing_points[n] = [int(cx), int(cy)]
                sorted_cross_points = sort_rectangle_contour(crossing_points)
                for n, p in enumerate(sorted_cross_points):
                    draw_str(grid, p[0], str(n))
                # imshow('grid', grid)
                solve_sudoku_ocr(transformed, sorted_cross_points)

    drawContours(frame, [sudoku_contour], 0, 255)
    imshow('Input', frame)


def solve_sudoku_ocr(src, crossing_points):
    '''
    Split the rectified sudoku image into smaller pictures of letters only.
    Then perform a ocr, create and solve the sudoku
    '''
    numbers = []
    for i, pos in enumerate([pos for pos in range(90) if (pos + 1) % 10 != 0]):
        square = np.float32([[-10, -10], [40, -10], [-10, 40], [40, 40]])
        quad = np.float32([crossing_points[pos],
                           crossing_points[pos + 1],
                           crossing_points[pos + 10],
                           crossing_points[pos + 11]])

        matrix = getPerspectiveTransform(quad, square)
        transformed = warpPerspective(src, matrix, (30, 30))

        #
        # ocr
        #
        ipl = iplimage_from_array(transformed)
        tesseract.SetCvImage(ipl, api)
        text = api.GetUTF8Text()
        # conf = api.MeanTextConf()
        # print '"%s" Confidence: %s' % (text.strip(), conf)

        #
        # Number conversion
        #
        try:
            n = int(text.strip())
            if not 0 < n < 10:
                return
            numbers.append(int(text.strip()))
        except:
            # skip the frame if ocr returned no number but we found a contour
            contours, _ = findContours(
                bitwise_not(transformed), RETR_TREE, CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                area = contourArea(cnt)
                if area > 100:
                    return
            numbers.append(0)

    for x in range(9):
        for y in range(9):
            number = numbers[y * 9 + x]
            if number == 0:
                continue
            draw_str(src, (75 + x * 50, 75 + y * 50), str(number))
    imshow('src', src)

    try:
        s = sudoku.Sudoku(numbers)
        s.solve()
        print s
        print ''
    except:
        pass  # no solutions found


def solve_sudoku_in_picture(filename):
    pic = imread(filename)
    process(pic)
    waitKey(0)


def solve_sudoku_in_video():
    cap = VideoCapture(0)
    while(True):
        _, frame = cap.read()
        process(frame)
        if waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()


if __name__ == '__main__':
    s = sudoku.Sudoku([0] * 81)

    api = tesseract.TessBaseAPI()
    api.Init(".", "eng", tesseract.OEM_DEFAULT)
    api.SetPageSegMode(tesseract.PSM_SINGLE_BLOCK)
    api.SetVariable("tessedit_char_whitelist", "0123456789")
    api.SetVariable("classify_enable_learning", "0")
    api.SetVariable("classify_enable_adaptive_matcher", "0")

    solve_sudoku_in_picture('pics/sudoku.jpg')
    # solve_sudoku_in_video()
    destroyAllWindows()

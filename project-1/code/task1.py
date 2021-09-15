import cv2 as cv
import numpy as np
from scipy import ndimage


def read_image_return_sudokut1(folder_path: str, filename: str) -> np.array:
    img = cv.imread(folder_path + "/" + filename, 0)
    img = cv.resize(img, (0, 0), fx=0.22, fy=0.22)
    original = img.copy()
    img = cv.GaussianBlur(img, (15, 15), 0)
    thresh = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                  cv.THRESH_BINARY, 5, 2)
    contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    saved = None
    for cnt in contours:
        x, y, w, h = cv.boundingRect(cnt)
        if w > 300 and w < 800 and h > 300 and h < 800:
            if saved is None:
                saved = (x, y, x + w, y + h)
            if saved[3] - saved[1] < h:
                saved = (x, y, x + w, y + h)
    if saved is not None:
        cv.rectangle(original, (saved[0], saved[1]), (saved[2], saved[3]), (0, 255, 0), 2)
    original = cv.adaptiveThreshold(original, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                    cv.THRESH_BINARY, 73, 35)
    if saved is None:
        return original
    else:
        return original[saved[1]:saved[3], saved[0]:saved[2]]


def rotate_sudoku(x: np.array) -> np.array:
    edges = cv.Canny(x, 50, 100, apertureSize=3)
    theta = cv.HoughLines(edges, 1, np.pi / 180, 200)
    if len(theta) >=16:
        theta = theta[15][0][1]
    else:
        theta = theta[-1][0][1]
    degree = theta * 57
    first = x.shape[0]
    if degree > 5 and degree < 30:
        x = ndimage.rotate(x, degree)
    if degree < 89 and degree > 31:
        x = ndimage.rotate(x, -(89 - degree))
    if degree > 92 and degree < 120:
        x = ndimage.rotate(x, abs(89 - degree))
    if degree > 121 and degree < 178:
        x = ndimage.rotate(x, -(180 - degree))
    diff = x.shape[0] - first
    if diff > 30:
        diff = diff // 2
        x = x[diff + 22:-(diff + 22), diff + 22:-(diff + 22)]
    return x


def extract_squares(rotate_sudoku: np.array) -> list:
    squares = []
    mock_image = rotate_sudoku.copy()
    mock_image = cv.adaptiveThreshold(mock_image, 255, cv.ADAPTIVE_THRESH_MEAN_C, \
                                      cv.THRESH_BINARY, 25, 11)
    contours, _ = cv.findContours(mock_image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x, y, w, h = cv.boundingRect(cnt)
        epsilon = 0.1 * cv.arcLength(cnt, True)
        approx = cv.approxPolyDP(cnt, epsilon, True)
        perimeter = cv.arcLength(cnt, True)
        if perimeter > 180 and perimeter < 300 and len(approx) == 4:
            saved = (x, y, x + w, y + h)
            squares.append(saved)
    return squares


def complete_squares(squares, img):
    squares = sorted(squares, key=lambda x: x[0])
    temp = sorted(squares, key=lambda x: x[1])
    a = [abs(temp[0][0] - temp[1][0]), abs(temp[0][1] - temp[1][1]), abs(temp[0][2] - temp[1][2]),
         abs(temp[0][3] - temp[1][3])]
    b = [abs(squares[0][0] - squares[1][0]), abs(squares[0][1] - squares[1][1]), abs(squares[0][2] - squares[1][2]),
         abs(squares[0][3] - squares[1][3])]
    if max(a) <= max(b):
        square_max = max(a) + 3
    else:
        square_max = max(b) + 3
    total = 0
    last = None
    fixed_sudoku = []
    square = []
    if len(squares) < 81:
        for i in squares:
            if last is None:
                total += 1
                last = i[0]
                square.append(i)
            elif len(square) == 9:
                fixed_sudoku.append(square)
                last = i[0]
                total = 1
                square = []
                square.append(i)
            elif last + 25 < i[0]:
                if total < 9:
                    timeout = 0
                    while len(square) != 9 and timeout != 100:
                        timeout += 1
                        square = sorted(square, key=lambda x: x[1])
                        min_y = min([x[1] for x in squares])
                        for j in range(len(square)):
                            if square[0][1] - 10 <= min_y:
                                if j != len(square) - 1 and len(square) < 9:
                                    if square[j + 1][1] - square[j][1] >= square_max + 12:
                                        elem = (square[j][0], square[j][3], square[j][2], square[j][3] + square_max - 6)
                                        square.insert(j + 1, elem)
                            else:
                                elem = (square[j][0], min_y, square[j][2], min_y + square_max)
                                square.insert(0, elem)
                        if len(square) == 9:
                            break
                        while len(square) < 9 and img.shape[0] - square[-1][3] + 10 >= square_max:
                            elem = (square[-1][0], square[-1][3], square[-1][2], square[-1][3] + square_max - 6)
                            square.append(elem)
                    if len(square) == 9:
                        fixed_sudoku.append(square)
                else:
                    fixed_sudoku.append(square)
                last = i[0]
                total = 1
                square = []
                square.append(i)
            else:
                last = i[0]
                square.append(i)
                total += 1
        if total != 9:
            timeout = 0
            while len(square) != 9 and timeout != 100:
                timeout += 1
                square = sorted(square, key=lambda x: x[1])
                min_y = min([x[1] for x in squares])
                for j in range(len(square)):
                    if square[0][1] - 10 <= min_y:
                        if j != len(square) - 1 and len(square) < 9:
                            if square[j + 1][1] - square[j][1] >= square_max:
                                elem = (square[j][0], square[j][3], square[j][2], square[j][3] + square_max - 6)
                                square.insert(j + 1, elem)
                    else:
                        elem = (square[j][0], min_y, square[j][2], min_y + square_max)
                        square.insert(0, elem)
                if len(square) == 9:
                    break
                while len(square) < 9 and img.shape[0] - square[-1][3] >= square_max:
                    elem = (square[-1][0], square[-1][3], square[-1][2], square[-1][3] + square_max - 6)
                    square.append(elem)
            if len(square) == 9:
                fixed_sudoku.append(square)
            else:
                pass
        else:
            fixed_sudoku.append(square)
        return fixed_sudoku
    return squares


def create_submision_template() -> list:
    template = '''
oooxxxooo
ooxoooxoo
xooooooox
oxoooooxo
oxoxxxoxo
oxoooooxo
xooooooox
ooxoooxoo
oooxxxooo'''
    template = template.replace("x", 'o').split("\n")[1:]
    template = [list(x) for x in template]
    return template


def create_submision(squares: list, image: np.array) -> list:
    img = image.copy()
    img = cv.bitwise_not(img)
    x = squares
    values = []
    if len(x) == 81:
        block = sorted(squares, key=lambda x: (x[0], x[1]))
        block = np.abs((np.array(block[0]) - np.array(block[1]))).max() - 1
        for s, y, w, h in sorted(squares, key=lambda x: (x[0], x[1])):
            uniq = np.unique(np.digitize(img[y + 8:h - 8, s + 8:w - 8], np.array([55])), return_counts=True)
            if s < block and s < block - 10:
                i = 0
            elif s > block - 10 and s < block:
                i = s // block + 1
            else:
                i = s // block
            if y < block and y < block - 10:
                j = 0
            elif y > block - 10 and y < block:
                j = y // block + 1
            else:
                j = y // block
            # print(i,j)
            if len(uniq[1]) == 2 and uniq[1][1] > 100:
                # print(j,i)
                values.append((j, i))
    else:
        new_list = []
        for item in x:
            for s in item:
                new_list.append(s)
        new_list = sorted(new_list, key=lambda x: (x[0], x[1]))
        block = sorted(new_list, key=lambda x: (x[0], x[1]))
        block = np.abs((np.array(block[0]) - np.array(block[1]))).max() - 1
        for s, y, w, h in new_list:
            if s < block and s < block - 10:
                i = 0
            elif s > block - 10 and s < block:
                i = s // block + 1
            else:
                i = s // block
            if y < block and y < block - 10:
                j = 0
            elif y > block - 10 and y < block:
                j = y // block + 1
            else:
                j = y // block

            uniq = np.unique(np.digitize(img[y + 8:h - 8, s + 8:w - 8], np.array([55])), return_counts=True)
            if len(uniq[1]) == 2 and uniq[1][1] > 100:
                values.append((j, i))
    return values


def make_prediction(x: list, output_path):
    submision = create_submision_template()
    first = np.array([y[0] for y in x])
    second = np.array([y[1] for y in x])
    if min(first) < 0:
        first += abs(min(first))
    if min(second) < 0:
        first += abs(min(second))
    if max(first) > 8:
        if 0 in first:
            first[first > 8] = 8
        else:
            first -= (max(first) - 8)
    if max(second) > 8:
        if 0 in second:
            second[second > 8] = 8
        else:
            second -= (max(second) - 8)

    for x, y in zip(first, second):
        submision[x][y] = 'x'
    out = ''
    for x in range(9):
        for y in range(9):
            out += submision[x][y]
        out += '\n'
    file = open(output_path, 'w+')
    file.writelines(out[:-1])
    file.close()

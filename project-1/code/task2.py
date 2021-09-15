import cv2 as cv
import numpy as np


def read_image_return_sudokut2(folder_path: str, filename: str) -> np.array:  # return sudoku area
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
    cv.rectangle(original, (saved[0], saved[1]), (saved[2], saved[3]), (0, 0, 0), 13)

    if saved is None:
        return original
    return original[saved[1]:saved[3], saved[0]:saved[2]]


def make_segmentation(classic_path: str,
                      filename: str) -> list:  # segments region of proeminent lines that define the jigsaw and sorted them left to right by index in square
    img = read_image_return_sudokut2(classic_path, filename)

    bw = cv.bitwise_not(img)
    ret, bw = cv.threshold(img, 200, 255, cv.THRESH_BINARY)

    horizontalStructure = cv.getStructuringElement(cv.MORPH_RECT, (4, 1))
    bw = cv.bitwise_not(img)
    horizontal = cv.erode(bw, horizontalStructure)
    horizontal = cv.dilate(horizontal, horizontalStructure)

    vertical = cv.getStructuringElement(cv.MORPH_RECT, (1, 4))
    horizontal = cv.erode(horizontal, vertical)
    horizontal = cv.dilate(horizontal, vertical)

    horizontal = cv.bitwise_not(horizontal)
    horizontal = cv.GaussianBlur(horizontal, (5, 5), 0)
    ret3, horizontal = cv.threshold(horizontal, 200, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    contours, _ = cv.findContours(horizontal, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cont = 0
    all_cont = []
    for cnt in contours:
        epsilon = 0.0002 * cv.arcLength(cnt, True)
        approx = cv.approxPolyDP(cnt, epsilon, True)
        if len(approx) > 4 and epsilon > 0.06:
            all_cont.append(np.array(approx))
            cont += 1
    all_cont = sorted(all_cont, key=lambda ctr: (cv.boundingRect(ctr)[1] // 45, cv.boundingRect(ctr)[0] // 45))
    return all_cont


def make_squares(classic_path: str, filename: str) -> list:  # extracts all squares in sudoku
    img = read_image_return_sudokut2(classic_path, filename)
    img = cv.GaussianBlur(img, (3, 3), 0)
    ret3, img = cv.threshold(img, 140, 255, cv.THRESH_BINARY)
    contours, _ = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    squares = 0
    all_cont = []
    for cnt in contours:
        x, y, w, h = cv.boundingRect(cnt)
        epsilon = 0.1 * cv.arcLength(cnt, True)
        approx = cv.approxPolyDP(cnt, epsilon, True)
        if len(approx) == 4 and w > 30 and h < 100:
            all_cont.append([x, y, x + w, y + h])
            squares += 1
    if squares != 81:
        img = read_image_return_sudokut2(classic_path, filename)
        img = cv.GaussianBlur(img, (3, 3), 0)
        ret3, img = cv.threshold(img, 170, 255, cv.THRESH_BINARY)

        contours, _ = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        squares = 0
        all_cont = []
        for cnt in contours:
            x, y, w, h = cv.boundingRect(cnt)
            epsilon = 0.1 * cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, epsilon, True)
            if len(approx) == 4 and w > 30 and h < 100:
                all_cont.append([x, y, x + w, y + h])
                squares += 1
        return all_cont
    else:
        return all_cont


def sort_squares(all_squares: list) -> list:  # sort the extracted squares in order of the the position
    correct = []
    for i in range(9):
        for j in range(9):
            correct.append([i, j])
    sorted_squares = []
    diff = sorted(all_squares, key=lambda y: (y[0]))
    block = diff[0][1] - diff[1][1] - 3
    predict = []
    for item in sorted(all_squares, key=lambda y: (y[0] // block, y[1] // block)):
        predict.append([item[0] // block, item[1] // block])
    if predict != correct:
        block = 52
        predict = []
        for item in sorted(all_squares, key=lambda y: (y[0] // block, y[1] // block)):
            predict.append([item[0] // block, item[1] // block])
        if predict == correct:
            return sorted(all_squares, key=lambda y: (y[0] // block, y[1] // block))
        else:
            return sorted(all_squares, key=lambda y: (y[0] // block, y[1] // block))
    return sorted(all_squares, key=lambda y: (y[0] // block, y[1] // block))


def create_submision_template() -> list:  # simple submision template
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


def prediction(classic_path: str, filename: str, sorted_square: list,
               segments: list) -> str:  # verify if is in a segmented zone and if there is a number in that square
    img = read_image_return_sudokut2(classic_path, filename)
    img = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, \
                               cv.THRESH_BINARY, 73, 35)
    img = cv.bitwise_not(img)
    subm = create_submision_template()
    count = 0
    for s, y, w, h in sorted_square:
        i, j = count % 9, count // 9
        in_y, in_x = y + 4, s + 4
        decision = 0
        for index, into in enumerate(segments):
            if cv.pointPolygonTest(into, (in_x, in_y), False) == 1:
                decision = index + 1
                break
        uniq = np.unique(np.digitize(img[y + 8:h - 8, s + 8:w - 8], np.array([55])), return_counts=True)
        if len(uniq[1]) == 2 and uniq[1][1] > 50:
            subm[i][j] = str(decision) + 'x'
        else:
            subm[i][j] = str(decision) + 'o'
        count += 1
    out = ''
    for x in range(9):
        for y in range(9):
            out += subm[x][y]
        out += '\n'
    return out


def write_prediction(out: str, output_path):
    file = open(output_path, 'w+')
    file.writelines(out)
    file.close()


from task1 import *
from task2 import *


def task1(classic_path: str, filename: str, out_folder: str):
    image = read_image_return_sudokut1(classic_path, filename)  # extract sudoku approx square
    image = rotate_sudoku(image)  # rotate to have the same orientation
    squares = extract_squares(image)  # extract squares of sudoku by bounding box
    squares = complete_squares(squares, image)  # complete missing squares that are not covered in the bounding box
    out = create_submision(squares, image)  # create submission based on difference of length of square
    try:
        make_prediction(out, out_folder + "/" + filename + ".txt")  # makes out file
    except:
        print("failed")


def task2(classic_path: str, filename: str, out_folder: str):
    segmentation = make_segmentation(classic_path, filename)  # extract sudoku approx square
    squares = make_squares(classic_path, filename)  # extract squares of sudoku by bounding box
    squares = sort_squares(squares)  # sort sudoku squares
    predict = prediction(classic_path, filename, squares,
                         segmentation)  # complete missing squares that are not covered in the bounding box
    write_prediction(predict, out_folder + "/" + filename + ".txt")


def verify(in_path: str, out_path: str, length: int):
    count = 0
    for i in range(1, length):
        file1 = open(in_path + str(i) + "_gt.txt")
        file2 = open(out_path + str(i) + ".jpg.txt")
        out1 = file1.readlines()
        out2 = file2.readlines()
        out1 = [x.replace("\n", '') for x in out1]
        out2 = [x.replace("\n", '') for x in out2]
        count += (out1 == out2)
        file1.close()
        file2.close()
    print("total correct - ", count)


if __name__ == '__main__':
    print("Start task 1")
    # for running task 1 and 2 an input path is need and a output path for writing files
    length_task_1 = 51
    length_task_2 = 41
    for i in range(1, length_task_1):
        # print(i)
        print('../test/classic'+str(i) + '.jpg')
        task1('../test/classic', str(i) + '.jpg', '../train/out')
    print("Start task 2")
    for i in range(1, length_task_2):
        # print(i)
        task2('../test/jigsaw', str(i) + '.jpg', '../train/out1')
    print("task 1")
    # for testing the parameters are input path for correct files, output files folder and amount of files (1.txt,2.txt....,51.txt)
    #verify('../train/classic/', "../train/out/", length_task_1)
    print("task 2") # at task 2 there may be an additional "\n" if something is not right
    #verify('../train/jigsaw/', "../train/out1/", length_task_2)
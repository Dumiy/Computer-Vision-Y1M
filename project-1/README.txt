Your project should include a README file containing the following information:

1. the libraries required to run the project including the full version of each library

Example:

numpy==1.19.5
opencv_python==4.2.0
scipy==1.3.1

2. how to run each task and where to look for the output file.

main.py contains running for task 1 and 2 and verification.

The changes that need to be done if first to give the input folder and the number of files with the formating of "1.jpg,2.jpg,3.jpg...n.jpg"
and the output for the desired output where out file are going to be written.

Task 1: 
script: task1.py
function: task1(classic_path: str, filename: str, out_folder: str), where classic_path is the path to the folder containing the images for task1
filename: file name from folder classic_path, format by name+".jpg"
out_folder: the output file is results/task1.txt

Task 2: task2(classic_path: str, filename: str, out_folder: str), where classic_path is the path to the folder containing the images for task1
filename: file name from folder classic_path, format by name+".jpg"
out_folder: output folder where files are going to be written for each image like "1.jpg.txt"

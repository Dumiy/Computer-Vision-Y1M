
1. the libraries required to run the project including the full version of each library

Example:

- opencv-python and opencv-contrib-python == 4.2.0
- numpy == 1.19.5
- os
- torchvision == 0.8.2+cu101
- torch == 1.7.1+cu101
- sklearn == 0.21.3

2. how to run each task and where to look for the output file.

The notebook contains all the needs for the project
Task 1:
For the tasks all the modification needed are for base_path at each tasks base_path = "train/Task1/", with any folder and to run the write prediction

Task 2: For the task all the modification needed are for base_path at each tasks base_path = "train/Task2/", with any folder and to run the write prediction

Task 3: For the task all the modification needed are for base_path at each tasks base_path = "train/Task3/", with any folder and to run the write prediction and run the cell 

Task 4: For the task all the modification needed are for base_path at each tasks base_path = "train/Task4/", with any folder and to run the next cell then it would be required to have the pretrained model on your local machine, load it and run the write prediction and submission cell or to train it with train test split 12 epochs with the given params.

The process is to transform the dataset from task4 into a object detection dataset, we take the video transform it to list of images with the labels or the bbox or [0,0,0,0] depending if curling rock is present or not. Then we resize the images by reducing them to 0.25 of the normal size, the labels will be divided by the size of the images to have them in range of the sigmoid values and then we train them with the respective settings in the notebook. At writing the submission files the [0,0,0,0] prediction made by the models are removed at writing to have a format same as the labels.


The output files for each task are present in evaluation/submission_files/Dumitrascu_Claudiu_Cristian_407/Task {1-4}
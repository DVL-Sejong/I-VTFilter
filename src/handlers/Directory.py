import os
import shutil
import src.handlers.Path as Path


def create_new_directories(csv_file_name, count_of_fixations):
    path = Path.get_origin_path(csv_file_name)
    for i in range(count_of_fixations):
        if os.path.exists(path + str(i)) is True:
            break
        else:
            os.mkdir(path + str(i))


def create_directory(csv_file_name):
    path = Path.get_path("result") if csv_file_name is "result" else Path.get_origin_path(csv_file_name)
    if os.path.exists(path) is not True:
        os.mkdir(path)


def is_result_exists(filename):
    path = Path.get_path("result") + filename
    return True if os.path.isfile(path) else False


def is_image_exists(image_name):
    path = Path.get_image_path(image_name)
    return True if os.path.isfile(path) else False


def move_image_files(csv_file_name, result_list):
    for i, result in enumerate(result_list):
        for j, value in enumerate(result):
            image_path = Path.get_origin_image_path(csv_file_name, value)
            destination_path = Path.get_destination_path(csv_file_name, i, value)
            shutil.move(image_path, destination_path)
            print(image_path, destination_path)
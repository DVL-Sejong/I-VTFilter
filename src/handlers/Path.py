import os
from os import listdir
from os.path import isfile, join


def get_destination_path(csv_file_path, number, threshold):
    file_name = csv_file_path.split(".")[0]
    path = "%s\\%d\\%s_%0.15f.png" % (get_origin_path(csv_file_path), number, file_name, float(threshold))
    return path


def get_origin_image_path(csv_file_path, threshold):
    file_name = csv_file_path.split(".")[0]
    path = "%s%s_%0.15f.png" % (get_origin_path(csv_file_path), file_name, float(threshold))
    return path


def get_origin_path(csv_file_path):
    return get_path("result\\" + csv_file_path.split(".")[0])


def get_file_names(directory):
    path = get_path(directory)
    files = [f for f in listdir(path) if isfile(join(path, f))]
    return files


def get_path(directory):
    path = os.path.dirname(os.path.realpath(__file__))
    path += "\\" + directory + "\\"
    return path


def get_image_path(filename):
    path = get_path("result") + filename + ".png"
    return path
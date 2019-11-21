from Data import GazeData
from VectorUtil import Point3D
import pandas as pd
import os
from os import listdir
from os.path import isfile, join


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


def load_gaze_data(file_name):
    path = get_path("data") + file_name
    raw_data = pd.read_csv(path, header=None, names=["id", "name", "time", "order", "x", "y"]).T.to_dict()
    data_list = dict_to_list(raw_data)
    return data_list


def dict_to_list(raw_data):
    data_list = []
    for i in range(len(raw_data)):
        id = raw_data[i]["id"]
        name = raw_data[i]["name"]
        time = raw_data[i]["time"]
        order = raw_data[i]["order"]
        point = Point3D(raw_data[i]["x"], raw_data[i]["y"], 9.100000381469727)
        gaze_data = GazeData(id, name, time, order, point)
        data_list.append(gaze_data)
    return data_list

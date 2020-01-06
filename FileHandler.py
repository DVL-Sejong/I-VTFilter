import numpy

import constant
from Data import RawData
import pandas as pd
from os import listdir
from os.path import isfile, join
import shutil
import os


# path
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


def get_result_path(csv_file_path):
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


def is_result_exists(filename):
    path = get_path("result") + filename
    print(path)
    return True if os.path.isfile(path) else False


# csv
def load_gaze_data(file_name):
    path = get_path("data") + file_name
    raw_data = RawData(pd.read_csv(path, header=None, names=["id", "name", "time", "order", "x", "y"]).T.to_dict())
    return raw_data.to_list()


def load_spectrum_raw_data(file_name):
    path = get_path("result") + file_name
    raw_data = pd.read_csv(path, header=None, names=['result', 'number_of_fixations']).drop_duplicates()
    dictionary = raw_data.to_dict('records')
    threshold, number_of_fixations = spectrum_dict_to_list(dictionary)
    return threshold, number_of_fixations


def save_data(threshold_and_number_of_fixations, file_name):
    path = get_path("result") + file_name + ".csv"
    threshold = [element[0] for element in threshold_and_number_of_fixations]
    number_of_fixations = [element[1] for element in threshold_and_number_of_fixations]
    dictionary = {
        'result': threshold,
        'number_of_fixations': number_of_fixations
    }
    dataframe = pd.DataFrame(dictionary)
    dataframe.to_csv(path, index=False, columns=['result', 'number_of_fixations'])


def save_statistics(csv_file_name, number_of_fixations, new_threshold):
    fixation_path = csv_file_name.split(".")[0] + "\\fixation_statistics.csv"
    velocity_path = csv_file_name.split(".")[0] + "\\velocity_statistics.csv"
    fixation_dictionary = {
        'fixation 평균 수': [sum(number_of_fixations, 0.0) / len(number_of_fixations)],
        'fixation 최소': [min(number_of_fixations)],
        'fixation 최대': [max(number_of_fixations)],
        'fixation 수 표준편차': [numpy.std(number_of_fixations)],
        'fixation 분산': [numpy.var(number_of_fixations)]
    }
    velocity_dictionary = {
        'velocity 갯수:': [len(number_of_fixations)],
        'velocity 평균': [numpy.mean(new_threshold)],
        'velocity 중앙값': [new_threshold[numpy.math.floor(len(new_threshold) / 2)]],
        'velocity 최소': [min(new_threshold)],
        'velocity 최대': [max(new_threshold)],
        'velocity 표준편차': [numpy.std(new_threshold)],
        'velocity 분산': [numpy.var(new_threshold)]
    }
    fixation_frame = pd.DataFrame(fixation_dictionary)
    fixation_frame.to_csv(fixation_path, index=False, columns=constant.FIXATION_COLUMNS)
    velocity_frame = pd.DataFrame(velocity_dictionary)
    velocity_frame.to_csv(velocity_path, index=False, columns=constant.VELOCITY_COLUMNS)


# directory/exists
def create_new_directories(csv_file_name, count_of_fixations):
    path = get_origin_path(csv_file_name)
    for i in range(count_of_fixations):
        if os.path.exists(path + str(i)) is True:
            break
        else:
            os.mkdir(path + str(i))


def create_directory(csv_file_name):
    path = get_path("result") if csv_file_name is "result" else get_result_path(csv_file_name)
    if os.path.exists(path) is not True:
        os.mkdir(path)


def is_image_exists(image_name):
    path = get_image_path(image_name)
    return True if os.path.isfile(path) else False;


# file moving
def move_image_files(csv_file_name, result_list):
    for i, result in enumerate(result_list):
        for j, value in enumerate(result):
            image_path = get_origin_image_path(csv_file_name, value)
            destination_path = get_destination_path(csv_file_name, i, value)
            shutil.move(image_path, destination_path)
            print(image_path, destination_path)


# 기타등등
def load_spectrum_data(csv_file_name):
    threshold, number_of_fixations = load_spectrum_raw_data(csv_file_name)
    result_list = construct_result_list(number_of_fixations)
    for velocity, count in zip(threshold, number_of_fixations):
        result_list[count].append(velocity)
    return result_list, max(number_of_fixations) + 1


def construct_result_list(number_of_fixations):
    biggest_fixation_number = max(number_of_fixations)
    result_list = []
    for i in range(biggest_fixation_number + 1):
        result_list.append([])
    return result_list


def spectrum_dict_to_list(raw_data):
    threshold_list = []
    count_list = []
    for i in range(1, len(raw_data)):
        threshold_list.append(raw_data[i]["result"])
        count_list.append(int(raw_data[i]["number_of_fixations"]))
    return threshold_list, count_list


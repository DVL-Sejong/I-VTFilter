import numpy
from src import constant
import pandas as pd
from src.objects.RawData import RawData
import src.handlers.Path as Path


def load_gaze_data(file_name):
    path = Path.get_path("data") + file_name
    raw_data = RawData(pd.read_csv(path, header=None, names=["id", "name", "time", "order", "x", "y"]).T.to_dict())
    return raw_data.to_list()


def load_spectrum_raw_data(file_name):
    path = Path.get_path("result") + file_name
    raw_data = pd.read_csv(path, header=None, names=['result', 'number_of_fixations']).drop_duplicates()
    dictionary = raw_data.to_dict('records')
    threshold, number_of_fixations = spectrum_dict_to_list(dictionary)
    return threshold, number_of_fixations


def save_data(threshold_and_number_of_fixations, file_name):
    path = Path.get_path("result") + file_name + ".csv"
    threshold = [element[0] for element in threshold_and_number_of_fixations]
    number_of_fixations = [element[1] for element in threshold_and_number_of_fixations]
    dictionary = {
        'result': threshold,
        'number_of_fixations': number_of_fixations
    }
    dataframe = pd.DataFrame(dictionary)
    dataframe.to_csv(path, index=False, columns=['result', 'number_of_fixations'])


def save_statistics(csv_file_name, number_of_fixations, new_threshold):
    fixation_path = Path.get_path("result") + "\\" + csv_file_name.split(".")[0] + "\\fixation_statistics.csv"
    velocity_path = Path.get_path("result") + "\\" + csv_file_name.split(".")[0] + "\\velocity_statistics.csv"
    fixation_dictionary = {
        'average number of fixations': [sum(number_of_fixations, 0.0) / len(number_of_fixations)],
        'minimum value of fixations': [min(number_of_fixations)],
        'maximum value of fixations': [max(number_of_fixations)],
        'standard deviation of number of fixations': [numpy.std(number_of_fixations)],
        'dispersion of fixation': [numpy.var(number_of_fixations)]
    }
    velocity_dictionary = {
        'number of velocities': [len(number_of_fixations)],
        'average of velocities': [numpy.mean(new_threshold)],
        'median': [new_threshold[numpy.math.floor(len(new_threshold) / 2)]],
        'minimum': [min(new_threshold)],
        'maximum': [max(new_threshold)],
        'standard deviation': [numpy.std(new_threshold)],
        'dispersion': [numpy.var(new_threshold)]
    }
    fixation_frame = pd.DataFrame(fixation_dictionary)
    fixation_frame.to_csv(fixation_path, index=False, columns=constant.FIXATION_COLUMNS)
    velocity_frame = pd.DataFrame(velocity_dictionary)
    velocity_frame.to_csv(velocity_path, index=False, columns=constant.VELOCITY_COLUMNS)


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


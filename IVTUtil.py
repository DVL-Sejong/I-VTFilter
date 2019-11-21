from VectorUtil import Point2D
import constant
import numpy as np
from Data import GazeData
import FileHandler
import Data
import VectorUtil as vu
import math


def classify_into_fixation(filename, frequency, threshold):
    gaze_data = FileHandler.load_gaze_data(filename)
    velocities = []

    buffer = []
    amplitude = []
    i = 0
    while True:
        if i + 1 < len(gaze_data):
            buffer.append(i)
            start, end = Data.get_consecutive_points(gaze_data, buffer, len(buffer) - 2)
            angular_distance = vu.get_angular_distance(constant.USER_ORIGIN, start, end)
            amplitude.append(angular_distance)
            i += 1

        first_id, last_id = Data.get_first_last_point_id(gaze_data, buffer)
        window = GazeData.subtract_time(first_id, last_id) / frequency

        if window < 1 and i + 1 >= len(gaze_data): break
        if window >= 1:
            velocity = sum(amplitude) / window
            velocities.append(velocity)
            gaze_data[buffer[0]].movement_type = constant.FIXATION if velocity < threshold else constant.SACCADE
            amplitude.pop(0)
            buffer.pop(0)

    velocities.sort()
    list(set(velocities))

    return gaze_data, velocities


def extract_fixation_saccade_centroid_line(gaze_data):
    fixation, saccade = get_fixation_and_saccade(gaze_data)
    centroids, line = get_centroids_and_line(gaze_data)
    return fixation, saccade, centroids, line


def get_saccade_line(centroids):
    lines = []
    for i in range(len(centroids) - 1):
        lines.append([[centroids[i].x, centroids[i].y], [centroids[i + 1].x, centroids[i + 1].y]])
    saccade_line = np.array(lines)
    return convert_line_into_point(saccade_line)


def convert_line_into_point(saccade_line):
    points = []
    if len(saccade_line) == 0: return points

    x_list = saccade_line[:, :, 0].T
    y_list = saccade_line[:, :, 1].T
    for i in range(len(x_list)):
        points.append(Point2D(x_list[i], y_list[i]))
    return points


def get_centroids_and_line(gaze_data):
    centroids = []
    index = 0

    while index < len(gaze_data) - 1:
        if gaze_data[index].movement_type is constant.FIXATION:
            centroid, index = centroid_of_fixation(gaze_data, index)
            centroids.append(centroid)
        elif gaze_data[index].movement_type is constant.SACCADE:
            index = get_first_fixation_index(gaze_data, index)
        else:
            break

    lines = get_saccade_line(centroids)
    return centroids, lines


def get_first_fixation_index(gaze_data, index):
    while gaze_data[index].movement_type is constant.SACCADE:
        index += 1
    return index


def centroid_of_fixation(gaze_data, index):
    count = 0
    x_sum = 0
    y_sum = 0
    while gaze_data[index].movement_type is constant.FIXATION:
        x_sum += gaze_data[index].point.x
        y_sum += gaze_data[index].point.y
        index += 1
        count += 1
    return Point2D(x_sum / count, y_sum / count), index


def get_fixation_and_saccade(gaze_data):
    fixation = []
    saccade = []
    for data in gaze_data:
        if data.movement_type is constant.FIXATION:
            fixation.append(data.point)
        elif data.movement_type is constant.SACCADE:
            saccade.append(data.point)
    return fixation, saccade

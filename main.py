from Data import GazeData
from Data import ClusteredData
from VectorUtil import Point2D
import matplotlib.pyplot as plt
import VectorUtil as vu
import numpy as np
import FileHandler
import constant
import math


def main():
    # 파일명 입력하고 데이터 파싱
    gaze_data = FileHandler.load_gaze_data("tdata1")
    velocities = []

    buffer = []
    amplitude = []
    i = 0
    eye_velocities = []
    median = 0
    while True:
        if i + 1 < len(gaze_data):
            buffer.append(i)
            amplitude.append(vu.get_angular_distance(constant.USER_ORIGIN, gaze_data[buffer[len(buffer) - 2]].point, gaze_data[buffer[len(buffer) - 1]].point))
            median = math.floor(len(buffer) / 2)
            i += 1

        window = GazeData.subtract_time(gaze_data[buffer[0]].id, gaze_data[buffer[len(buffer) - 1]].id) / 60

        if window < 1 and i + 1 >= len(gaze_data): break
        if window >= 1:
            velocity = sum(amplitude) / window
            velocities.append(velocity)
            eye_velocities.append([velocity, buffer[median]])
            gaze_data[buffer[0]].movement_type = constant.FIXATION if velocity < 12 else constant.SACCADE
            amplitude.pop(0)
            buffer.pop(0)

    filename = ""
    centroids, lines = get_centroids_and_line(gaze_data)
    fixation, saccade = get_fixation_and_saccade(gaze_data)
    plot_filtered_data(constant.PLOT_IMAGE, fixation, saccade, centroids, filename)


def get_fixation_and_saccade(gaze_data):
    fixation = []
    saccade = []
    for data in gaze_data:
        if data.movement_type is constant.FIXATION:
            fixation.append(data.point)
        elif data.movement_type is constant.SACCADE:
            saccade.append(data.point)
    return fixation, saccade


def plot_filtered_data(plot_type, fixation, saccade, centroids, filename):
    line_x, line_y = get_saccade_line(centroids)
    fig, ax = plt.subplots()
    img = plt.imread("image\\test.png")
    ax.imshow(img, extent=[0, 1920, 0, 1080], alpha=0.5, origin='lower')

    plt.plot(line_x, line_y, color='black')
    plt.scatter([sac.x for sac in saccade], [sac.y for sac in saccade], color='black', alpha=0.5)
    plt.scatter([fix.x for fix in fixation], [fix.y for fix in fixation], color='red', alpha=0.5)
    plt.scatter([center.x for center in centroids], [center.y for center in centroids], color='blue', s=80)

    plt.title("Fixtation detected")
    plt.xlabel("X axis")
    plt.ylabel("Y axis")
    plt.gca().invert_yaxis()

    if plot_type is constant.PLOT_IMAGE: plt.show()
    else: plt.savefig(FileHandler.get_image_path(filename))


def get_saccade_line(centroids):
    lines = []
    for i in range(len(centroids) - 1):
        lines.append([[centroids[i].x, centroids[i].y], [centroids[i + 1].x, centroids[i + 1].y]])
    saccade_line = np.array(lines)

    x_list = saccade_line[:, :, 0].T
    y_list = saccade_line[:, :, 1].T
    return x_list, y_list


def get_centroids_and_line(gaze_data):
    centroids = []
    lines = []
    index = 0

    while index < len(gaze_data) - 1:
        if gaze_data[index].movement_type is constant.FIXATION:
            centroid, index = centroid_of_fixation(gaze_data, index)
            centroids.append(centroid)
        elif gaze_data[index].movement_type is constant.SACCADE:
            start, end, index = get_line_edges(gaze_data, index)
            lines.append([start, end])
        else:
            break
    return centroids, lines


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


def get_line_edges(gaze_data, index):
    start = gaze_data[index].point
    while gaze_data[index].movement_type is constant.SACCADE:
        index += 1
    end = gaze_data[index - 1].point
    return start, end, index


def is_same_type(previous, current):
    return True if previous.movement_type is current.movement_type else False


def is_reverse_type(previous, current):
    if previous.movement_type is constant.UNKNOWN or current.movement_type is constant.UNKNOWN:
        return False
    if previous.movement_type is not current.movement_type:
        return True
    return False


def get_points(gaze_data, index):
    point1 = Point2D(gaze_data[index]["x"], gaze_data[index]["y"])
    point2 = Point2D(gaze_data[index + 1]["x"], gaze_data[index + 1]["y"])
    return point1, point2


if __name__ == "__main__":
    main()

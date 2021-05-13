import src.constant
from VectorUtil import Point3D, Point2D
import VectorUtil as vu
import numpy as np


class IVTData:
    def __init__(self, gaze_datas, frequency, threshold):
        self.gaze_datas = gaze_datas
        self.frequency = frequency
        self.threshold = threshold
        self.velocities = []
        self.amplitudes = []
        self.buffer = []
        self.window = 0
        self.index = 0

    def is_iterating(self):
        return True if self.index + 1 < len(self.gaze_datas) else False

    def is_over(self):
        return True if self.window < 1 and self.index + 1 >= len(self.gaze_datas) else False

    def is_window_more_than_a_second(self):
        return True if self.window >= 1 else False

    def append_buffer(self):
        self.buffer.append(self.index)

    def append_amplitude(self):
        point1, point2 = self.get_last_consecutive_points()
        angular_distance = vu.get_angular_distance(constant.USER_ORIGIN, point1, point2)
        self.amplitudes.append(angular_distance)

    def append_velocity(self):
        velocity = sum(self.amplitudes) / self.window
        self.velocities.append(velocity)

    def increase_index(self):
        self.index += 1

    def calculate_angular_distance(self):
        self.append_buffer()
        self.append_amplitude()
        self.increase_index()

    def get_velocity(self):
        return self.velocities[len(self.velocities) - 1]

    def set_velocity_and_type(self):
        self.append_velocity()
        self.set_movement_type()

    def sort_velocities(self):
        self.velocities.sort()
        list(set(self.velocities))

    def set_movement_type(self):
        velocity = self.get_velocity()
        self.gaze_datas[self.buffer[0]].movement_type = constant.FIXATION if velocity < self.threshold else constant.SACCADE
        self.amplitudes.pop(0)
        self.buffer.pop(0)

    def set_window(self):
        first_id, last_id = self.get_first_last_point_id()
        self.window = (last_id - first_id) / self.frequency

    def get_last_consecutive_points(self):
        current_index = self.buffer[len(self.buffer) - 2]
        last_index = self.buffer[len(self.buffer) - 1]
        point1 = self.gaze_datas[current_index].point
        point2 = self.gaze_datas[last_index].point
        return point1, point2

    def get_first_last_point_id(self):
        first_index = self.buffer[0]
        last_index = self.buffer[len(self.buffer) - 1]
        return self.gaze_datas[first_index].id, self.gaze_datas[last_index].id


class AnalyzedData:
    def __init__(self, gaze_datas, velocities):
        self.gaze_datas = gaze_datas
        self.velocities = velocities
        self.fixations = []
        self.saccades = []
        self.centroids = []
        self.centroids_lines = []
        self.fixation_index = 0

    def init_datas(self):
        while self.fixation_index < len(self.gaze_datas) - 1:
            if self.gaze_datas[self.fixation_index].movement_type is constant.FIXATION:
                centroid = self.centroid_of_fixation()
                self.centroids.append(centroid)
            elif self.gaze_datas[self.fixation_index].movement_type is constant.SACCADE:
                self.set_saccades()
            else:
                break
        self.set_centroids_lines()

    def centroid_of_fixation(self):
        count = 0
        x_sum = 0
        y_sum = 0
        while self.gaze_datas[self.fixation_index].movement_type is constant.FIXATION:
            x_sum += self.gaze_datas[self.fixation_index].point.x
            y_sum += self.gaze_datas[self.fixation_index].point.y
            self.fixations.append(self.gaze_datas[self.fixation_index].point)
            self.fixation_index += 1
            count += 1
        return Point2D(x_sum / count, y_sum / count)

    def set_saccades(self):
        while self.gaze_datas[self.fixation_index].movement_type is constant.SACCADE:
            self.saccades.append(self.gaze_datas[self.fixation_index].point)
            self.fixation_index += 1

    def set_centroids_lines(self):
        lines = []
        for i in range(len(self.centroids) - 1):
            start = [self.centroids[i].x, self.centroids[i].y]
            end = [self.centroids[i + 1].x, self.centroids[i + 1].y]
            lines.append([start, end])
        array_line = np.array(lines)
        self.to_point(array_line)

    def to_point(self, array_line):
        if len(array_line) == 0: return

        x_list = array_line[:, :, 0].T
        y_list = array_line[:, :, 1].T
        for i in range(len(x_list)):
            self.centroids_lines.append(Point2D(x_list[i], y_list[i]))

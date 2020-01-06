import numpy as np
from src import constant
from src.objects.Point2D import Point2D


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

from src import constant
import src.objects.Point3D as p3d


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
        angular_distance = p3d.get_angular_distance(constant.USER_ORIGIN, point1, point2)
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
import constant


class GazeData:
    def __init__(self, id, name, time, order, point):
        self.id = id
        self.name = name
        self.time = time
        self.order = order
        self.point = point
        self.movement_type = constant.UNKNOWN

    @staticmethod
    def subtract_time(start, end):
        return end - start


def get_consecutive_points(gaze_data, buffer, index):
    current_index = buffer[index]
    next_index = buffer[index + 1]
    point1 = gaze_data[current_index].point
    point2 = gaze_data[next_index].point
    return point1, point2


def get_first_last_point_id(gaze_data, buffer):
    first_index = buffer[0]
    last_index = buffer[len(buffer) - 1]
    return gaze_data[first_index].id, gaze_data[last_index].id

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


class ClusteredData:
    def __init__(self, movement_type, gaze_list):
        self.movement_type = movement_type
        self.gaze_list = gaze_list

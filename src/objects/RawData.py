from src import constant
from src.objects.Point3D import Point3D


class RawData:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.gaze_datas = []

    def to_list(self):
        for i in range(len(self.raw_data)):
            id = self.raw_data[i]["id"]
            name = self.raw_data[i]["name"]
            time = self.raw_data[i]["time"]
            order = self.raw_data[i]["order"]
            point = Point3D(self.raw_data[i]["x"], self.raw_data[i]["y"], constant.USER_DISTANCE)
            gaze_data = GazeData(id, name, time, order, point)
            self.gaze_datas.append(gaze_data)
        return self.gaze_datas


class GazeData:
    def __init__(self, id, name, time, order, point):
        self.id = id
        self.name = name
        self.time = time
        self.order = order
        self.point = point
        self.movement_type = constant.UNKNOWN

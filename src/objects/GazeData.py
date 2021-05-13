class GazeData:
    def __init__(self, id, name, time, order, point):
        self.id = id
        self.name = name
        self.time = time
        self.order = order
        self.point = point
        self.movement_type = 0

    @staticmethod
    def subtract_time(start, end):
        return end - start

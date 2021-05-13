import math
import numpy as np


class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_length(self):
        return np.sqrt(np.power(self.x, 2) + np.power(self.y, 2))

    @staticmethod
    def get_distance(point1, point2):
        subtracted = Point2D.subtract(point1, point2)
        return math.sqrt(math.pow(subtracted.x), 2, math.pow(subtracted.y), 2)

    @staticmethod
    def subtract(point1, point2):
        return Point2D(point1.x - point2.x, point1.y - point2.y)

    @staticmethod
    def get_angle(point1, point2):
        cosine = Point2D.dot_product(point1, point2) / (point1.get_length() * point2.get_length())
        cosine = min(1, max(-1, cosine))
        return math.acos(cosine)

    @staticmethod
    def dot_product(point1, point2):
        return (point1.x * point2.x) + (point1.y * point2.y)
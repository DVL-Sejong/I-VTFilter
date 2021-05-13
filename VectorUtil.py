import math
from src.objects import Point3D, Point2D


def get_angular_distance(user_origin, start, end):
    start_vector = Point3D.normalize_vector(user_origin, start)
    end_vector = Point3D.normalize_vector(user_origin, end)

    if math.isnan(start_vector.x) or math.isnan(end_vector.x):
        return 0

    angle_radian = Point3D.get_angle(start_vector, end_vector)
    angle_degree = math.degrees(angle_radian)
    return angle_degree














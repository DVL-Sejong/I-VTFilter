from Data import IVTData


def classify_gaze_data(gaze_datas, frequency, threshold):
    ivt_data = IVTData(gaze_datas, frequency, threshold)

    while True:
        if ivt_data.is_iterating():
            ivt_data.calculate_angular_distance()
        ivt_data.set_window()
        if ivt_data.is_over(): break
        if ivt_data.is_window_more_than_a_second():
            ivt_data.set_velocity_and_type()

    ivt_data.sort_velocities()
    return ivt_data.gaze_datas, ivt_data.velocities

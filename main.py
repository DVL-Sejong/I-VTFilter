from src.handlers import File, Image, Path, Directory
from src import constant
from src.objects.AnalyzedData import AnalyzedData
from src.objects.IVTData import IVTData


def get_unanalyzed_filenames():
    files = Path.get_file_names("data")

    unanalyzed_files = []
    for file in files:
        if Directory.is_result_exists(file): continue
        unanalyzed_files.append(file)

    return unanalyzed_files


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


def preprocess_data(filenames):
    preprocessed_data = []
    for file in filenames:
        gaze_data = File.load_gaze_data(file)
        classified_data, velocities = classify_gaze_data(gaze_data, constant.FREQUENCY, constant.BASIC_THRESHOLD)
        preprocessed_data.append([file, gaze_data, velocities])
    return preprocessed_data


def analyze_and_save_data(preprocessed_data):
    for file, gaze_data, velocities in preprocessed_data:
        csv_result = analyze_gaze_data(file, gaze_data, velocities)
        File.save_data(csv_result, file.split(".")[0])


def analyze_gaze_data(file, gaze_data, velocities):
    csv_result = []
    for cnt, threshold in enumerate(velocities):
        saving_filename = "%s\\%s_%0.15f" % (file.split(".")[0], file.split(".")[0], threshold)
        classified_data, velocities = classify_gaze_data(gaze_data, constant.FREQUENCY, threshold)
        analyzed_data = AnalyzedData(classified_data, velocities)
        analyzed_data.init_datas()
        Image.plot_filtered_data(constant.SAVE_IMAGE, analyzed_data, saving_filename)
        csv_result.append([threshold, len(analyzed_data.centroids)])
        print(saving_filename, threshold, len(analyzed_data.centroids))
    return csv_result


def classify_images():
    files = Path.get_file_names("result")

    for i, csv_file_name in enumerate(files):
        result_list, count_of_fixations = File.load_spectrum_data(csv_file_name)
        Directory.create_new_directories(csv_file_name, count_of_fixations)

        if Directory.is_image_exists(csv_file_name.split(".")[0] + "\\fixation_numbers"):
            continue

        Directory.move_image_files(csv_file_name, result_list)

        threshold, number_of_fixations = File.load_spectrum_raw_data(csv_file_name)
        Image.plot_fixation_numbers(threshold, number_of_fixations, csv_file_name)
        new_threshold = [float(element) for element in threshold]
        File.save_statistics(csv_file_name, number_of_fixations, new_threshold)


if __name__ == "__main__":
    names = get_unanalyzed_filenames()
    Directory.preprocess_directories(names)
    preprocessed_data = preprocess_data(names)
    analyze_and_save_data(preprocessed_data)
    classify_images()

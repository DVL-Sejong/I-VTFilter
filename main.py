import IVTUtil as ivt
import ImageHandler
import FileHandler
import constant
from Data import AnalyzedData


def get_unanalyzed_filenames():
    files = FileHandler.get_file_names("data")

    names = []
    for file in files:
        if FileHandler.is_result_exists(file): continue
        names.append(file)

    return names


def preprocess_directories(filenames):
    FileHandler.create_directory("result")
    for name in filenames: FileHandler.create_directory(name)


def preprocess_data(filenames):
    preprocessed_data = []
    for file in filenames:
        gaze_data = FileHandler.load_gaze_data(file)
        classified_data, velocities = ivt.classify_gaze_data(gaze_data, constant.FREQUENCY, constant.BASIC_THRESHOLD)
        preprocessed_data.append([file, gaze_data, velocities])
    return preprocessed_data


def analyze_and_save_data(preprocessed_data):
    for file, gaze_data, velocities in preprocessed_data:
        csv_result = analyze_gaze_data(file, gaze_data, velocities)
        FileHandler.save_data(csv_result, file.split(".")[0])


def analyze_gaze_data(file, gaze_data, velocities):
    csv_result = []
    for cnt, threshold in enumerate(velocities):
        saving_filename = "%s\\%s_%0.15f" % (file.split(".")[0], file.split(".")[0], threshold)
        classified_data, velocities = ivt.classify_gaze_data(gaze_data, constant.FREQUENCY, threshold)
        analyzed_data = AnalyzedData(classified_data, velocities)
        analyzed_data.init_datas()
        ImageHandler.plot_filtered_data(constant.SAVE_IMAGE, analyzed_data, saving_filename)
        csv_result.append([threshold, len(analyzed_data.centroids)])
        print(saving_filename, threshold, len(analyzed_data.centroids))
    return csv_result


def classify_images():
    files = FileHandler.get_file_names("result")

    for i, csv_file_name in enumerate(files):
        result_list, count_of_fixations = FileHandler.load_spectrum_data(csv_file_name)
        FileHandler.create_new_directories(csv_file_name, count_of_fixations)

        if FileHandler.is_image_exists(csv_file_name.split(".")[0] + "\\fixation_numbers"):
            continue

        FileHandler.move_image_files(csv_file_name, result_list)

        threshold, number_of_fixations = FileHandler.load_spectrum_raw_data(csv_file_name)
        ImageHandler.plot_fixation_numbers(threshold, number_of_fixations, csv_file_name)
        new_threshold = [float(element) for element in threshold]
        FileHandler.save_statistics(csv_file_name, number_of_fixations, new_threshold)


if __name__ == "__main__":
    names = get_unanalyzed_filenames()
    preprocess_directories(names)
    preprocessed_data = preprocess_data(names)
    analyze_and_save_data(preprocessed_data)
    classify_images()

import IVTUtil as ivt
import ImageHandler
import FileHandler
import constant
import numpy
import math


def main():
    files = FileHandler.get_file_names("result")

    for i, csv_file_name in enumerate(files):
        if csv_file_name.split(".")[1] != "csv": continue
        threshold, number_of_fixatoins = FileHandler.load_spectrum_raw_data(csv_file_name)
        ImageHandler.plot_fixation_numbers(threshold, number_of_fixatoins, csv_file_name)
        new_threshold = [float(element) for element in threshold]
        print(csv_file_name.split(".")[0])
        print("velocity 갯수: %d" % len(number_of_fixatoins))
        print("fixation 평균 수: %f " % (sum(number_of_fixatoins, 0.0) / len(number_of_fixatoins)))
        print("fixation 최소: %d" % min(number_of_fixatoins))
        print("fixation 최대: %d" % max(number_of_fixatoins))
        print("fixation 수 표준편차: %f" % numpy.std(number_of_fixatoins))
        print("fixation 수 분산: %f" % numpy.var(number_of_fixatoins))
        print("velocity 평균: %f " % numpy.mean(new_threshold))
        print("velocity 중앙값: %f " % new_threshold[math.floor(len(new_threshold)/2)])
        print("velocity 최소: %d" % min(new_threshold))
        print("velocity 최대: %d" % max(new_threshold))
        print("velocity 표준편차: %f" % numpy.std(new_threshold))
        print("velocity 분산: %f" % numpy.var(new_threshold))


def move_images():
    files = FileHandler.get_file_names("result")

    for i, csv_file_name in enumerate(files):
        result_list, count_of_fixations = FileHandler.load_spectrum_data(csv_file_name)
        FileHandler.create_new_directories(csv_file_name, count_of_fixations)
        FileHandler.move_image_files(csv_file_name, result_list)


def analyze_raw_gaze_data():
    files = FileHandler.get_file_names("data")

    for index, file in enumerate(files):
        if index != 7: continue
        threshold_and_number_of_fixations = []
        classified_data, velocities = ivt.classify_into_fixation(file, constant.FREQUENCY, constant.BASIC_THRESHOLD)
        FileHandler.create_directory(file)
        for cnt, threshold in enumerate(velocities):
            saving_filename = "%s\\%s_%0.15f" % (file.split(".")[0], file.split(".")[0], threshold)
            classified_data, angular_velocities = ivt.classify_into_fixation(file, constant.FREQUENCY, threshold)
            fixation, saccade, centroids, line, parts = ivt.extract_fixation_saccade_centroid_line(classified_data)
            ImageHandler.plot_filtered_data(constant.SAVE_IMAGE, classified_data, fixation, saccade, centroids, line, parts, saving_filename)
            threshold_and_number_of_fixations.append([threshold, len(centroids)])
            print(saving_filename, threshold, len(centroids))
        FileHandler.save_data(threshold_and_number_of_fixations, file.split(".")[0])


if __name__ == "__main__":
    # analyze_raw_gaze_data()
    move_images()
    main()

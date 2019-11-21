import IVTUtil as ivt
import ImageHandler
import FileHandler
import constant


def main():
    analyze_raw_gaze_data()


def analyze_raw_gaze_data():
    files = FileHandler.get_file_names("data")

    for file in files:
        threshold_and_number_of_fixations = []
        classified_data, velocities = ivt.classify_into_fixation(file, constant.FREQUENCY, constant.BASIC_THRESHOLD)
        for threshold in velocities:
            saving_filename = "%s\\%s_%0.15f" % (file.split(".")[0], file.split(".")[0], threshold)
            classified_data, angular_velocities = ivt.classify_into_fixation(file, constant.FREQUENCY, threshold)
            fixation, saccade, centroids, line = ivt.extract_fixation_saccade_centroid_line(classified_data)
            ImageHandler.plot_filtered_data(constant.SAVE_IMAGE, fixation, saccade, centroids, line, saving_filename)
            threshold_and_number_of_fixations.append([threshold, len(centroids)])
            print(saving_filename, threshold, len(centroids))
        FileHandler.save_data(threshold_and_number_of_fixations, file.split(".")[0])


if __name__ == "__main__":
    main()

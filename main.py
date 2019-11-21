import IVTUtil as ivt
import ImageHandler
import FileHandler
import constant


def main():
    files = FileHandler.get_file_names("data")

    for file in files:
        threshold = 30
        for count in range(100):
            if count == 1: threshold = median
            elif count != 0: threshold -= 0.02
            saving_filename = file.split(".")[0] + "_" + str(threshold)
            classified_data, median = ivt.classify_into_fixation(file, constant.FREQUENCY, threshold)
            fixation, saccade, centroids, line = ivt.extract_fixation_saccade_centroid_line(classified_data)
            ImageHandler.plot_filtered_data(constant.SAVE_IMAGE, fixation, saccade, centroids, line, saving_filename)
            print(saving_filename)


if __name__ == "__main__":
    main()

from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import FileHandler
import constant
import numpy


def plot_filtered_data(plot_type, analyzed_data, filename):
    if plot_type is constant.SAVE_IMAGE and FileHandler.is_image_exists(filename): return

    fig, ax = plt.subplots()
    background = plt.imread("image\\i-vt_image_re.png")
    ax.imshow(background, extent=[0, 1920, 0, 1080], alpha=0.5, origin='lower')

    line = analyzed_data.centroids_lines if analyzed_data.centroids_lines is not None else []
    saccade = analyzed_data.saccades
    fixation = analyzed_data.fixations
    centroids = analyzed_data.centroids if analyzed_data.centroids is not None else []

    plt.plot([point.x for point in line], [point.y for point in line], color='black')
    plt.scatter([sac.x for sac in saccade], [sac.y for sac in saccade], color='black', alpha=0.5)
    plt.scatter([fix.x for fix in fixation], [fix.y for fix in fixation], color='black', alpha=0.5)
    plt.scatter([center.x for center in centroids], [center.y for center in centroids], color='blue', s=80)

    plt.title("Fixtation detected")
    plt.xlabel("X axis")
    plt.xticks()
    plt.ylabel("Y axis")
    plt.gca().invert_yaxis()

    if plot_type is constant.PLOT_IMAGE: plt.show()
    else: plt.savefig(FileHandler.get_image_path(filename))


def plot_fixation_numbers(result_list, count_of_fixations, csv_file_name):
    figure(num=None, figsize=(12, 10), dpi=80, facecolor='w', edgecolor='k')
    path = csv_file_name.split(".")[0] + "\\fixation_numbers"
    plt.scatter([index for index in result_list], [count for count in count_of_fixations], color='black', alpha=0.5)
    plt.title("Fixtation numbers")
    plt.xlabel("X axis")
    plt.xticks(numpy.arange(0, len(result_list), step=50), [index for index in result_list], rotation=75)
    plt.ylabel("Y axis")
    plt.savefig(FileHandler.get_image_path(path))
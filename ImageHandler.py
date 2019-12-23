from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import FileHandler
import constant
import numpy
from random import randint


def generate_color():
    colors = []
    for i in range(30):
        colors.append('#%06X' % randint(0, 0xFFFFFF))
    return colors


def plot_filtered_data(plot_type, classified_data, fixation, saccade, centroids, line, parts, filename):
    fig, ax = plt.subplots()
    img = plt.imread("image\\i-vt_image_re.png")
    ax.imshow(img, extent=[0, 1920, 0, 1080], alpha=0.5, origin='lower')

    plt.plot([point.x for point in line], [point.y for point in line], color='black')
    plt.scatter([sac.x for sac in saccade], [sac.y for sac in saccade], color='black', alpha=0.5)
    plt.scatter([fix.x for fix in fixation], [fix.y for fix in fixation], color='black', alpha=0.5)
    plt.scatter([center.x for center in centroids], [center.y for center in centroids], color='blue', s=80)

    # colors = generate_color()
    # for c, part in enumerate(parts):
    #     start = part[0]
    #     end = part[1]
    #     x_list = []
    #     y_list = []
    #     for index in range(start, end + 1):
    #         x_list.append(classified_data[index].point.x)
    #         y_list.append(classified_data[index].point.y)
    #     plt.scatter(x_list, y_list, color=colors[c % 30], alpha=0.5)
    #     # print(str(c % 10))



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
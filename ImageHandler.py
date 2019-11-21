import matplotlib.pyplot as plt
import FileHandler
import constant


def plot_filtered_data(plot_type, fixation, saccade, centroids, line, filename):
    fig, ax = plt.subplots()
    img = plt.imread("image\\test.png")
    ax.imshow(img, extent=[0, 1920, 0, 1080], alpha=0.5, origin='lower')

    plt.plot([point.x for point in line], [point.y for point in line], color='black')
    plt.scatter([sac.x for sac in saccade], [sac.y for sac in saccade], color='black', alpha=0.5)
    plt.scatter([fix.x for fix in fixation], [fix.y for fix in fixation], color='red', alpha=0.5)
    plt.scatter([center.x for center in centroids], [center.y for center in centroids], color='blue', s=80)

    plt.title("Fixtation detected")
    plt.xlabel("X axis")
    plt.ylabel("Y axis")
    plt.gca().invert_yaxis()

    if plot_type is constant.PLOT_IMAGE: plt.show()
    else: plt.savefig(FileHandler.get_image_path(filename))

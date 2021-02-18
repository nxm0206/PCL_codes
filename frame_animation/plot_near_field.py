import numpy as np
import cv2
import matplotlib.pyplot as plt

from matplotlib.ticker import MaxNLocator

from glob import glob



def plot_nearfield(filename):




    img = cv2.imread(filename, 0)
    height, width = img.shape
    print(height,width)
    pix_height = 130
    pix_width = 320
    zi = np.zeros([pix_height, pix_width])
    print(zi.shape)

    x_start = 0
    y_start = 20


    for m in range(pix_width):
        for n in range(pix_height):
            zi[n][m] = img[y_start+n][x_start+m]/np.max(img)




    xi = np.linspace(0, 500, pix_width)
    yi = np.linspace(0, 203, pix_height)


    X, Y = np.meshgrid(xi, yi)


    levels = MaxNLocator(nbins=255).tick_values(0, np.max(zi))

    fig1, ax1 = plt.subplots(figsize=(7,2.5),gridspec_kw={'hspace': 0.8, 'bottom': 0.24,'left': 0.2})

    image = ax1.contourf(X, Y, zi, levels=levels)

    ax1.set_xlabel(r'$\theta$ direction ($\mu$m)', fontsize=16)
    ax1.set_ylabel(r'$\varphi$ direction ($\mu$m)', fontsize=16)
    cbar = fig1.colorbar(image, ticks=[0, 0.5, 1])
    cbar.ax.set_ylabel(r'Intensity (a.u.)', fontsize=16)

    ticklabs = cbar.ax.get_yticklabels()

    ax1.tick_params(axis='both', which='major', labelsize=14)
    cbar.ax.set_yticklabels(ticklabs, fontsize=14)


filename_list = glob('D:/measurement_data/20201124/real_space/plot/*.bmp')

for i in range(len(filename_list)):

    plot_nearfield(filename_list[i])

plt.show()



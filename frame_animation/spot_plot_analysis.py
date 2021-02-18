import numpy as np
import cv2
import matplotlib.pyplot as plt

from matplotlib.ticker import MaxNLocator
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from glob import glob
from matplotlib.ticker import MultipleLocator


def get_column(matrix, i, n):
    if n == 0:
        return [row[i] for row in matrix]
    return [np.mean(row[int(i-n):int(i+n)]) for row in matrix]


def get_row(matrix, i):
    return matrix[i]


def sinc_fit(x, a, b, x0, l1, l2):
    return a*np.sinc(b*(x-x0))**2+l1*x+l2

def double_sinc_fit(x, a1, b1, x01, a2, b2, x02, l1, l2):
    return a1*np.sinc(b1*(x-x01))**2+a2*np.sinc(b2*(x-x02))**2+l1*x+l2


def polynomial_function(x, x0, x1, x2):
    return x2*x**2 + x1*x**1 + x0


def gauss_function(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))


def lin_interp(x, y, i, half):
    return x[i] + (x[i+1] - x[i]) * ((half - y[i]) / (y[i+1] - y[i]))


def half_max_x(x, y):
    half = max(y)/2.0
    signs = np.sign(np.add(y, -half))
    zero_crossings = (signs[0:-2] != signs[1:-1])
    zero_crossings_i = np.where(zero_crossings)[0]
    if len(zero_crossings_i) < 2:
        return[0, 0]
    else:
        return [lin_interp(x, y, zero_crossings_i[0], half),lin_interp(x, y, zero_crossings_i[1], half)]


def plot_2D_color(X, Y, Z, x_label, y_label, z_label, n_col, n_row):
    fig, ax1 = plt.subplots(gridspec_kw={'bottom': 0.2, 'left': 0.2})

    X_grid, Y_grid = np.meshgrid(X, Y)
    levels = MaxNLocator(nbins=200).tick_values(0, np.max(Z))
    image = ax1.contourf(X_grid, Y_grid, Z, levels=levels)

    ax1.set_xlabel(x_label, fontsize=20)
    ax1.set_ylabel(y_label, fontsize=20)

    cbar = fig.colorbar(image, ticks=[0, 0.5, 1])
    ticklabs = cbar.ax.get_yticklabels()
    cbar.ax.set_yticklabels(ticklabs, fontsize=18)
    cbar.ax.set_ylabel(z_label, fontsize=20)
    # ax1.plot([X[n_col], X[n_col]], [np.min(Y), np.max(Y)], lw=0.3, c="r",
    #          ls='--')
    # ax1.plot([np.min(X), np.max(X)], [Y[n_row], Y[n_row]], lw=0.3, c="r",
    #          ls='--')

    ax1.set_xticklabels([40, 20, 0, -20])
    ax1.tick_params(axis='both', which='major', labelsize=18)
    ax1.tick_params(axis='both', which='minor', bottom='on')
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(5))


def plot_1Dx2(X1, Y1, X1_fit, Y1_fit, X1_peaks, Y1_peaks, x1_label, y1_label,
              X2, Y2, X2_fit, Y2_fit, X2_peaks, Y2_peaks, x2_label, y2_label):
    # plot data
    fig, (ax1, ax2) = plt.subplots(2, gridspec_kw={'hspace': 0.4, 'wspace': 0})
    ax1.plot(X1, Y1, 'o')
    ax1.plot(X1_fit, Y1_fit, '-', label='fit')
    ax1.plot(X1_peaks, Y1_peaks, 'x')
    ax1.set_xlabel(x1_label, fontsize=15)
    ax1.set_ylabel(y1_label, fontsize=15)
    ax2.plot(X2, Y2, 'o')
    ax2.plot(X2_fit, Y2_fit, '-', label='fit')
    ax2.plot(X2_peaks, Y2_peaks, 'x')
    ax2.set_xlabel(x2_label, fontsize=15)
    ax2.set_ylabel(y2_label, fontsize=15)


def remove_saturation(x_array, y_array, saturation_level):

    index_saturated = np.where(y_array >= saturation_level)[0]

    if len(index_saturated) <= 2:
        x_interp, y_interp = x_array, y_array

    else:

        x_list = np.asarray([x_array[index_saturated[0] - 1], x_array[index_saturated[0]],
                             x_array[index_saturated[-1]], x_array[index_saturated[-1] + 1]])
        y_list = np.asarray([y_array[index_saturated[0] - 1], y_array[index_saturated[0]],
                             y_array[index_saturated[-1]], y_array[index_saturated[-1] + 1]])

        popt, pcov = curve_fit(polynomial_function, x_list, y_list, p0=[1, 0, 0])
        # print(popt)
        x_interp, y_interp = np.copy(x_array), np.copy(y_array)
        for index in index_saturated:
            y_interp[index] = polynomial_function(x_array[index], *popt)

    return [x_interp, y_interp]


def figure_analysis(filename, pix_radius, NA, shift_row, shift_col, shift_x, shift_y):

    img = cv2.imread(filename, 0)
    height, width = img.shape
    zi = np.zeros([pix_radius, pix_radius])

    # find pixel position of x,y axis
    x_center = int(height/2.0) + shift_x
    y_center = int(width/2.0) + shift_y

    x_start = int(x_center - pix_radius/2)
    y_start = int(y_center - pix_radius/2)

    for m in range(pix_radius):
        for n in range(pix_radius):
            zi[m][n] = img[x_start+m][y_start+n]/np.max(img)

    x_sum = np.sum(zi, axis=0)
    y_sum = np.sum(zi, axis=1)
    py_axis = np.where(x_sum == x_sum.max())[0][0]
    px_axis = np.where(y_sum == y_sum.max())[0][0]

    n_row = px_axis+shift_row
    n_col = py_axis+shift_col

    xi = np.linspace(-NA, NA, pix_radius)
    yi = np.linspace(-NA, NA, pix_radius)

    xi_deg = np.arcsin(xi)*180/np.pi
    yi_deg = np.arcsin(yi)*180/np.pi

    X_grid, Y_grid = np.meshgrid(xi_deg, yi_deg)
    circle_outer = np.sqrt(X_grid**2+Y_grid**2) > np.arcsin(NA)*180/np.pi
    zi[circle_outer] = np.min(zi)*0.1

    # ====plot 2D =======================================================================
    if True:
        x_label = r'$\theta(^\circ)$'
        y_label = r'$\varphi(^\circ)$'
        z_label = r'Intensity (a.u.)'
        plot_2D_color(xi_deg, yi_deg, zi, x_label, y_label, z_label, n_col, n_row)

    # ============= improve data by remove saturated data =====================================
    if True:
        column_to_plot = np.asarray(get_column(zi, n_col, 1))*np.max(img)
        row_to_plot = np.asarray(get_row(zi, n_row))*np.max(img)
        saturation_level = 254
        [xi_deg_interp, column_interp] = remove_saturation(xi_deg, column_to_plot, saturation_level)
        [yi_deg_interp, row_interp] = remove_saturation(yi_deg, row_to_plot, saturation_level)

    # ============= fit sinc for vertical line ==============================================
    if True:
        fit_range = 10
        xi_fit = np.linspace(-fit_range, fit_range, 1000)
        x = xi_deg_interp
        y = column_interp
        popt, pcov = curve_fit(sinc_fit, x, y, p0=[500, 1, -0.3, 0.005, 10])
        column_fit = sinc_fit(xi_fit, *popt)
        # print(popt)

        from scipy.signal import find_peaks
        peaks_x, _ = find_peaks(column_fit, height=30, distance=50)
        phi_peak = xi_fit[peaks_x]

    # ==================== calculate FWHM ==========================================
    if True:
        hmx = half_max_x(xi_fit, column_fit)
        fwhm = hmx[1]-hmx[0]
        print("FWHM:{:.4f}".format(fwhm))

    # ====fit sinc for horizontal line===============================================
    if True:
        x = yi_deg_interp
        y = row_interp
        x0 = x[np.where(y == np.max(y))[0]]

        yi_fit = np.linspace(np.arcsin(-NA)*180/np.pi, np.arcsin(NA)*180/np.pi, 3000)
        popt, pcov = curve_fit(double_sinc_fit, x, y, p0=[200, 1, x0[0], 10, 0.5, -x0[0], -0.005, 10])
        row_fit = double_sinc_fit(yi_fit, *popt)
        # print(popt)

        peaks_y1, _ = find_peaks(row_fit, height=np.max(row_fit)*0.9, distance=50)
        fit_range = np.where((yi_fit > -x0[0] - 2) & (yi_fit < -x0[0] + 2))[0]
        peaks, _ = find_peaks(row_fit[fit_range], height=[np.mean(row_fit[fit_range]), np.max(row_fit[fit_range])*1.1], distance=50)

        peaks_y2 = np.where(yi_fit == yi_fit[fit_range[peaks]])[0]
        peaks_y = np.concatenate((peaks_y1, peaks_y2))

        theta_peak = yi_fit[peaks_y]
        print(theta_peak)

    # ====plot 1D =======================================================================
    if True:
        x1_label = r'$\varphi(deg)$'
        y1_label = r'Intensity (a.u.)'

        x2_label = r'$\theta(deg)$'
        y2_label = r'Intensity (a.u.)'

        plot_1Dx2(xi_deg, column_to_plot, xi_fit, column_fit, xi_fit[peaks_x], column_fit[peaks_x],
                  x1_label, y1_label,
                  yi_deg, row_to_plot, yi_fit, row_fit, yi_fit[peaks_y], row_fit[peaks_y],
                  x2_label, y2_label)

    return fwhm, theta_peak, phi_peak


if __name__ == '__main__':

    filename_list = glob('D:/measurement_data/20201201/spot/*.bmp')
    pix_radius = 216
    NA = 0.54
    spot_theta = []
    spot_wav = []
    wav = np.linspace(1449, 1651, (1652-1449))
    shift_row = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    shift_col = [0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0]
    shift_x = [0, 0, -2, -2, -2, -3, -1, -1, -1, -1, -1, -1]
    shift_y = [-7, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9]

    for i in range(1, 2):
        print(int(filename_list[i][-8:-4]))

        spot_size, theta_peak, phi_peak = figure_analysis(filename_list[i], pix_radius, NA, shift_row[i], shift_col[i], shift_x[i], shift_y[i])
        # print(theta_peak, phi_peak)
        spot_theta.append(theta_peak[0])
        spot_wav.append(int(filename_list[i][-8:-4]))

    # fig3, ax3 = plt.subplots(figsize=(7,2.5),gridspec_kw={'hspace': 0.8, 'bottom': 0.24,'left': 0.2})
    # # print(spot_wav, spot_theta)
    # ax3.plot(spot_wav, spot_theta, '-o')
    # ax3.set_xlabel(r'wavelength (nm)', fontsize=16)
    # ax3.set_ylabel(r'$\theta$ ($^\circ$)', fontsize=16)
    # ax3.tick_params(axis='both', which='major', labelsize=14)
    plt.show()



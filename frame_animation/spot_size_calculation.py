import numpy as np
import cv2
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from glob import glob

def get_column(matrix, i, n):
    if n == 0:
        return [row[i] for row in matrix]
    return [np.mean(row[int(i-n):int(i+n)]) for row in matrix]


def get_row(matrix, i):
    return matrix[i]


def sinc_fit(x, a, b, x0, l1, l2):
    return a*np.sinc(b*(x-x0))**2+l1*x+l2

# define functions for FWHM calculation
def lin_interp(x, y, i, half):
    return x[i] + (x[i+1] - x[i]) * ((half - y[i]) / (y[i+1] - y[i]))


def half_max_x(x, y):
    half = max(y)/2.0
    signs = np.sign(np.add(y, -half))
    zero_crossings = (signs[0:-2] != signs[1:-1])
    zero_crossings_i = np.where(zero_crossings)[0]
    return [lin_interp(x, y, zero_crossings_i[0], half),
            lin_interp(x, y, zero_crossings_i[1], half)]


def get_fwhm(filename, pix_radius, NA):


    img = cv2.imread(filename, 0)
    height, width = img.shape
    # pix_radius = 200
    zi = np.zeros([pix_radius, pix_radius])

    # find pixel position of x axis
    x_center = int(height/2.0)
    y_center = int(width/2.0)

    x_start = int(x_center - pix_radius/2)
    y_start = int(y_center - pix_radius/2)


    for m in range(pix_radius):
        for n in range(pix_radius):
            zi[m][n] = img[x_start+m][y_start+n]


    x_sum = np.sum(zi, axis=0)
    y_sum = np.sum(zi, axis=1)
    py_axis = np.where(x_sum == x_sum.max())[0][0]
    px_axis = np.where(y_sum == y_sum.max())[0][0]



    n_row = px_axis
    n_col = py_axis


    xi = np.linspace(-NA, NA, pix_radius)
    yi = np.linspace(-NA, NA, pix_radius)



    column_to_plot = np.asarray(get_column(zi, n_col, 1))
    row_to_plot = np.asarray(get_row(zi, n_row))

    # pop out saturated values
    saturation_level = 250
    index_saturated = np.where(column_to_plot >= saturation_level)[0]
    column_to_interp = np.delete(column_to_plot, index_saturated)
    xi_to_interp = np.delete(xi, index_saturated)
    f2 = interp1d(xi_to_interp, column_to_interp, kind='cubic')
    xi_interp = np.linspace(xi.min(), xi.max(), 10*pix_radius)
    column_interp = f2(xi_interp)


    #  fit sinc
    fit_range = 0.1
    xi_fit = np.linspace(-fit_range, fit_range, 1000)
    column_to_fit = f2(xi_fit)
    popt, pcov = curve_fit(sinc_fit, xi_fit, column_to_fit, p0=[max(column_interp), 100, -0.01, -0.3, 8.0])
    column_fit = sinc_fit(xi_fit, *popt)
    print(popt)

    # calculate FWHM
    hmx = half_max_x(xi_fit, column_fit)
    fwhm = (np.arcsin(hmx[1]) - np.arcsin(hmx[0]))*180/np.pi
    print("FWHM:{:.4f}".format(fwhm))

    return fwhm


filename_list = glob('D:/measurement_data/20201201/*.bmp')
pix_radius = 216
NA = 0.54
spot_FWHM = []
spot_wav = []
wav = np.linspace(1449, 1651, (1652-1449))

for fn in filename_list:
    print(int(fn[-8:-4]))
    spot_FWHM.append(get_fwhm(fn, pix_radius, NA))
    spot_wav.append(int(fn[-8:-4]))

fig, ax = plt.subplots()

ax.plot(spot_wav, spot_FWHM, 'o', label='measurement')
ax.set_ylim(0.2, 1.2)
ax.plot(wav, 0.886*wav/1000/126.5*180/np.pi, label='simulation')
ax.legend(fontsize=12)
ax.set_ylabel(r'$\varphi_{FWHM} (deg)$', fontsize=15)
ax.set_xlabel(r'wavelength(nm)', fontsize=15)
plt.show()



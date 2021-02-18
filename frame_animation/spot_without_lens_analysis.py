import numpy as np
import cv2
import matplotlib.pyplot as plt

from matplotlib.ticker import MaxNLocator
from scipy.optimize import curve_fit
from spot_plot_analysis import remove_saturation
from scipy.interpolate import interp1d


def get_column(matrix, i, n):
    return [np.mean(row[int(i-n):int(i+n)]) for row in matrix]


def get_row(matrix, i):
    return matrix[i]


def lin_interp(x, y, i, half):
    return x[i] + (x[i+1] - x[i]) * ((half - y[i]) / (y[i+1] - y[i]))


def half_max_x(x, y):
    half = max(y)/2.0
    signs = np.sign(np.add(y, -half))
    zero_crossings = (signs[0:-2] != signs[1:-1])
    zero_crossings_i = np.where(zero_crossings)[0]
    return [lin_interp(x, y, zero_crossings_i[0], half),
            lin_interp(x, y, zero_crossings_i[1], half)]


#  define sinc
def sinc_fit(x, a, b, x0, l1, l2):
    return a*np.sinc(b*(x-x0))**2+l1*x+l2

filename = 'D:/measurement_data/20201208/1610.bmp'
img = cv2.imread(filename, 0)

height, width = img.shape
zi = img
x_center = int(height/2.0)
y_center = int(width/2.0)
x_start = 0
y_start = 0

x_sum = np.sum(zi, axis=0)
y_sum = np.sum(zi, axis=1)
py_axis = np.where(x_sum == x_sum.max())[0][0]
px_axis = np.where(y_sum == y_sum.max())[0][0]

n_row = px_axis
n_col = py_axis

xi = np.linspace(-width/2.0, width/2.0-1, width)*0.03
yi = np.linspace(-height/2.0, height/2.0-1, height)*0.03

X, Y = np.meshgrid(xi, yi)

levels = MaxNLocator(nbins=256).tick_values(0, zi.max())


fig1, ax1 = plt.subplots()

image = ax1.contourf(X, Y, zi, levels=levels)

ax1.set_xlabel(r'$\theta$ direction(mm)')
ax1.set_ylabel(r'$\varphi$ direction(mm)')
cbar = fig1.colorbar(image)
cbar.ax.set_ylabel(r'Intensity (a.u.)')
ax1.plot([xi[n_col], xi[n_col]], [np.min(yi), np.max(yi)], lw=1, c="r", ls='--')
ax1.plot([np.min(xi), np.max(xi)], [yi[n_row], yi[n_row]], lw=1, c="r", ls='--')
plt.show()

# =============== plot cross-section ==================================
column_to_plot = np.asarray(get_column(zi, n_col, 1))
row_to_plot = np.asarray(get_row(zi, n_row))

# ==============distance between camera sensor and chip ========================
distance = 103.28-94.16+20.96
# ==============distance between camera sensor and chip ========================

# =============== fit alone phi direction ==================================
# pop out saturated values
saturation_level = 254
[yi_interp, column_interp] = remove_saturation(yi, column_to_plot, saturation_level)
f2 = interp1d(yi_interp, column_interp, kind='linear')


fit_range = 2
yi_fit = np.linspace(-fit_range, fit_range, 1000)
column_to_fit = f2(yi_fit)
popt, pcov = curve_fit(sinc_fit, yi_fit, column_to_fit, p0=[max(column_interp), 100, -0.007, -0.3, 8.0])
column_fit = sinc_fit(yi_fit, *popt)
# print(popt)

# calculate FWHM
hmx = half_max_x(yi_fit, column_fit)
fwhm = hmx[1]-hmx[0]
D_phi = np.arctan(fwhm/2.0/distance)*180/np.pi*2
print("FWHM:{:.4f}".format(fwhm))
print("phi_FWHM:{:.4f}".format(D_phi))


# =============== fit peak along theta direction ==================================
from scipy.signal import find_peaks
peak_index, _ = find_peaks(row_to_plot, height=30, distance=50)

# =============== calculate theta ==================================
peak_values = row_to_plot[peak_index]
first_largest = peak_values[np.where(peak_values==np.max(peak_values))[0]]
peak_values_cache = np.delete(peak_values, np.where(peak_values == np.max(peak_values))[0])
second_largest = peak_values[np.where(peak_values==np.max(peak_values_cache))[0]]
peaks1 = np.where(row_to_plot == first_largest)[0][0]
peaks2 = np.where(row_to_plot == second_largest)[0][0]
peaks = [peaks1, peaks2]
print(xi[peaks1], xi[peaks2])
L = abs(peaks1-peaks2)*30/1000.0
theta = np.arctan(L/2.0/distance)*180/np.pi
print(theta)


# plot data
fig2, (ax1, ax2) = plt.subplots(2, gridspec_kw={'hspace': 0.3, 'wspace': 0})
ax1.plot(yi, column_to_plot, '-')
# ax1.plot(yi_interp, column_interp, '-', label='interp')
ax1.plot(yi_fit, column_fit, '--', label='fit')
ax1.set_xlabel(r'$\varphi$ direction(mm)')
ax1.set_ylabel(r'Intensity (a.u.)')
ax2.plot(xi, get_row(zi, n_row))
ax2.plot(xi[peaks], row_to_plot[peaks], "x")
ax2.set_xlabel(r'$\theta$ direction(mm)')
ax2.set_ylabel(r'Intensity (a.u.)')
plt.show()








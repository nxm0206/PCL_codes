import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# import data from Excel file
# file_loc = "C:/Users/Nie/Desktop/Git Folder/code/simulation.xlsx"
file_loc = "D:/simulation/SOI_antenna/simulation.xlsx"
df = pd.read_excel(file_loc, sheet_name='Sheet2')
dperiod = 10.0
period = np.linspace(580, 780, int((780 - 580) / 10.0 + 1))
# print(period)
# print(dperiod)
dw = df.iloc[0:36, 1].values * 10 ** 9
ddw = dw[1]-dw[0]
# print(dw)
# print(ddw)
period_1d = df.iloc[0:757, 0].values * 10 ** 9
dw_1d = df.iloc[0:757, 1].values * 10 ** 9
neff_1d = df.iloc[0:757, 2].values
t10_1d = df.iloc[0:757, 3].values
angle_1d = df.iloc[0:757, 4].values
for i in range(len(t10_1d)):
    if t10_1d[i] >= 1.0:
        t10_1d[i] = 0.9999

# 2d color map function
def plot_2d(x, y, z, z_label, x_line, y_line):
    fig0, ax0 = plt.subplots(figsize=(9, 5), gridspec_kw={'bottom': 0.15, 'left': 0.15})
    clevel = [-30,8,10,30]
    cs = ax0.contourf(x, y, z, levels=clevel, origin='lower', extend='both')
    ax0.grid(c='k', ls='-', alpha=0.3)

    x_min, xmax, x_step = 10, 360, 10
    y_min, ymax, y_step = 580, 780, 10


    ax0.set_xlim(x_min, xmax)
    ax0.set_ylim(y_min, ymax)
    ax0.set_xticks(np.linspace(x_min, xmax, x_step).tolist())
    ax0.set_yticks(np.linspace(y_min, ymax, y_step).tolist())


    y_label = r'dw (nm)'
    x_label = r'period (nm)'
    # z_label = r'perturbation (dB/$\mu$m)'

    cbar0 = fig0.colorbar(cs)
    ticklabs = cbar0.ax.get_yticklabels()
    cbar0.ax.set_yticklabels(ticklabs, fontsize=14)
    cbar0.ax.set_ylabel(z_label, fontsize=14)

    ax0.scatter(x_line, y_line)
    ax0.set_ylabel(x_label, fontsize=14)
    ax0.set_xlabel(y_label, fontsize=14)

def plot_1d(x, y, x_label, y_label, x_scatter, y_scatter):
    fig0, ax0 = plt.subplots(figsize=(9, 5), gridspec_kw={'bottom': 0.15, 'left': 0.15})
    ax0.plot(x, y)
    # plt.scatter(beta_list, dw_list, marker ="^")
    ax0.scatter(x_scatter, y_scatter, marker="+")

    # clevel = 50
    # cs = ax0.contourf(x, y, z, levels=clevel, origin='lower', extend='both')
    ax0.grid(c='k', ls='-', alpha=0.3)

    x_min, xmax, x_step = np.min([np.min(x), np.min(x_scatter)]), np.max([np.max(x), np.max(x_scatter)]), 10
    y_min, ymax, y_step = np.min([np.min(y), np.min(y_scatter)]), np.max([np.max(y), np.max(y_scatter)]), 10


    ax0.set_xlim(x_min, xmax)
    ax0.set_ylim(y_min, ymax)
    ax0.set_xticks(np.linspace(x_min, xmax, x_step).tolist())
    ax0.set_yticks(np.linspace(y_min, ymax, y_step).tolist())


    # y_label = r'dw (nm)'
    # x_label = r'period (nm)'
    # # z_label = r'perturbation (dB/$\mu$m)'

    # cbar0 = fig0.colorbar(cs)
    # ticklabs = cbar0.ax.get_yticklabels()
    # cbar0.ax.set_yticklabels(ticklabs, fontsize=14)
    # cbar0.ax.set_ylabel(z_label, fontsize=14)

    # ax0.plot(x_line, y_line)
    ax0.set_xlabel(x_label, fontsize=14)
    ax0.set_ylabel(y_label, fontsize=14)


y_period = []
x_dw = []
z_beta =[]
theta_1d = np.arcsin(neff_1d - 1550 / period_1d) * 180 / np.pi
beta_1d = 10 * np.log10((1 - t10_1d) / (10 * period_1d * 10 ** (-3)))
angle_range = [8.0, 10.0]
# print(theta_1d)
for i in range(len(theta_1d)):
    if theta_1d[i] >= angle_range[0] and theta_1d[i] < angle_range[1]:
        y_period.append(period_1d[i])
        x_dw.append(dw_1d[i])
        z_beta.append(beta_1d[i])



p_min = np.min(y_period)
p_max = np.max(y_period)
period_list = np.linspace(p_min, p_max, int((p_max-p_min)/10.0+1))
# print(period_list)
dw_list = np.zeros_like(period_list)
beta_list = np.zeros_like(dw_list)





for j in range(len(period_list)):
    dw_samep = []
    beta_samep = []
    for i in range(len(x_dw)):
        if abs(y_period[i] - period_list[j]) <= 0.001:
            dw_samep.append(x_dw[i])
            beta_samep.append(z_beta[i])
            # dperiod.append(abs(y_period[i]-p_dw(dw_list[j], a1, b1, c1)))
    dw_list[j] = np.mean(dw_samep)
    beta_list[j] = np.mean(beta_samep)


p_dw_fit = np.polyfit(x_dw, y_period, 3)
p_dw = np.poly1d(p_dw_fit)
print(p_dw)
x_line = np.arange(min(x_dw), max(x_dw), 0.01)
y_line = p_dw(x_line)


def dw_beta(x, a, b, c, d, e):
    # a, b, c = paras
    # y = a/x**2 + b*x**2 + c*x + d
    # y = a*np.exp(b*x) + c + d
    # y = a*b**x + c
    y = a/x +b*x + c*np.exp(d*x) + e
    return y



popt, _ = curve_fit(dw_beta, z_beta, x_dw)
# dw_beta = np.poly1d(dw_beta_fit)
print(popt)
a, b, c, d, e = popt

# popt1, _ = curve_fit(p_dw, dw_list, period_list)
# a1, b1, c1, d1 = popt1
# print("p_dw:" + str(a1) + "x^2+" + str(b1) + "x+" + str(c1))
x_line_dw = np.arange(np.min(x_dw), np.max(x_dw), 0.01)
y_line_p = p_dw(x_line_dw)

x_line_beta = np.arange(np.min(z_beta), np.max(z_beta), 0.01)
y_line_dw = dw_beta(x_line_beta, a, b, c, d, e)

# dw_list = np.arange(min(x_dw), max(x_dw), dw[1]-dw[0])
# period_list = np.zeros_like(dw_list)
# beta_list = np.zeros_like(dw_list)
# for j in range(len(dw_list)):
#     period_samedw = []
#     dperiod = []
#     for i in range(len(x_dw)):
#         if abs(x_dw[i] - dw_list[j]) <= 0.001:
#             period_samedw.append(y_period[i])
#             dperiod.append(abs(y_period[i]-p_dw(dw_list[j], a1, b1, c1)))
#     period_list[j] = period_samedw[np.argmin(np.asarray(dperiod))]
#
#
plot_1d(x_line_dw, y_line_p, r'dw (nm)', r'period (nm)', x_dw, y_period)
plot_1d(x_line_beta, y_line_dw, r'beta (dB/$\mu$m)', r'dw (nm)', z_beta, x_dw)
# plt.plot(x_line_dw, y_line_p)
# # plt.scatter(dw_list, period_list, marker ="^")
# plt.scatter(x_dw, y_period, marker ="+")
# plt.show()

# plt.plot(x_line_beta, y_line_dw)
# # plt.scatter(beta_list, dw_list, marker ="^")
# plt.scatter(z_beta, x_dw, marker ="+")
# plt.show()

# for j in range(len(dw_list)):
#     for i in range(len(beta_1d)):
#         if abs(dw_1d[i] - dw_list[j]) <=0.001 and abs(period_1d[i] - period_list[j]) <=0.001:
#             beta_list[j] = beta_1d[i]
#
# def dw_beta(x, a2, b2, c2):
#     return a2 * x ** 2 + b2 * x + c2
# popt2, _ = curve_fit(dw_beta, beta_list, dw_list)
# a2, b2, c2 = popt2
# print("dw_beta:" + str(a2) + "x^2+" + str(b2) + "x+" + str(c2))
# x_line = np.arange(min(beta_list), max(beta_list), 0.01)
# y_line = dw_beta(x_line, a2, b2, c2)
# plt.plot(x_line, y_line)
# plt.scatter(beta_list, dw_list)
# plt.show()




neff_2d = np.reshape(np.asarray(neff_1d), [len(period), len(dw)])
t10_2d = np.reshape(np.asarray(t10_1d), [len(period), len(dw)])
angle_2d = np.reshape(np.asarray(angle_1d), [len(period), len(dw)])



X, Y = np.meshgrid(dw, period)
beta_2d = 10 * np.log10((1 - t10_2d) / (10 * Y * 10 ** (-3)))
theta_2d = np.arcsin(neff_2d - 1550 / Y) * 180 / np.pi
Z1 = beta_2d
Z2 = theta_2d
Z3 = angle_2d

# fit 2d data beta(period, dw)

# def beta_p_dw(M, a2, b2, c2, d2, e2, f2, g2, h2, i2, j2):
#     x, y = M
#     beta = a2 * x ** 3 + b2 * y ** 3 + c2 * x ** 2 * y + d2 * x * y ** 2 + e2 * x ** 2 + f2 * y ** 2 + g2 * x * y + h2 * x + i2 * y + j2
#
#     return beta
#
# xdata = np.vstack((X.ravel(), Y.ravel()))
# popt2, _ = curve_fit(beta_p_dw, xdata, Z1.ravel())
# a2, b2, c2, d2, e2, f2, g2, h2, i2, j2 = popt2
#
# Z4 = beta_p_dw(xdata, a2, b2, c2, d2, e2, f2, g2, h2, i2, j2)
# Z4 = np.reshape(Z4, [len(period), len(dw)])

# print(Y)
plot_2d(x=X, y=Y, z=Z1, x_line=x_dw, y_line=y_period, z_label='perturbation (dB/$\mu$m)')
# plot_2d(x=X, y=Y, z=Z2, x_line=x_line, y_line=y_line, z_label=r'calculated theta (degree)')
plot_2d(x=X, y=Y, z=Z3, x_line=x_dw, y_line=y_period, z_label=r'simulated theta (degree)')

# plot_2d(X, Y, abs(Z4-Z1), r'fitted perturbation (dB/$\mu$m)')



plt.show()

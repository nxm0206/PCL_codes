import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

file_loc = "D:/simulation/SOI_antenna/simulation.xlsx"
df = pd.read_excel(file_loc, sheet_name='Sheet1')
period = np.linspace(580, 780, int((780 - 580) / 10.0 + 1))
dw = df.iloc[0:36, 1].values * 10 ** 9
print(dw)
period_1d = df.iloc[0:757, 0].values * 10 ** 9
dw_1d = df.iloc[0:757, 1].values * 10 ** 9
neff_1d = df.iloc[0:757, 2].values
t10_1d = df.iloc[0:757, 3].values
angle_1d = df.iloc[0:757, 4].values
for i in range(len(t10_1d)):
    if t10_1d[i] >= 1.0:
        t10_1d[i] = 0.9999

y_period = []
x_dw = []
theta_1d = np.arcsin(neff_1d - 1550 / period_1d) * 180 / np.pi
beta_1d = 10 * np.log10((1 - t10_1d) / (10 * period_1d * 10 ** (-3)))
print(theta_1d)
for i in range(len(theta_1d)):
    if theta_1d[i] <= 16.5 and theta_1d[i] >= 15.5:
        y_period.append(period_1d[i])
        x_dw.append(dw_1d[i])


def p_dw(x, a1, b1, c1):
    return a1 * x ** 2 + b1 * x + c1



popt1, _ = curve_fit(p_dw, x_dw, y_period)
a1, b1, c1 = popt1
print("p_dw:" + str(a1) + "x^2+" + str(b1) + "x+" + str(c1))
x_line = np.arange(min(x_dw), max(x_dw), 0.01)
y_line = p_dw(x_line, a1, b1, c1)

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
# plt.plot(x_line, y_line)
# plt.scatter(dw_list, period_list, marker ="^")
# plt.scatter(x_dw, y_period)
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


fig1, ax1 = plt.subplots(figsize=(9, 5), gridspec_kw={'bottom': 0.15, 'left': 0.15})
clevel = 50
cs = ax1.contourf(X, Y, Z1, levels=clevel)

y_label = r'dw (nm)'
x_label = r'period (nm)'
z_label = r'perturbation (dB/$\mu$m)'

cbar1 = fig1.colorbar(cs)
ticklabs = cbar1.ax.get_yticklabels()
cbar1.ax.set_yticklabels(ticklabs, fontsize=14)
cbar1.ax.set_ylabel(z_label, fontsize=14)

ax1.set_ylabel(x_label, fontsize=14)
ax1.set_xlabel(y_label, fontsize=14)

fig2, ax2 = plt.subplots(figsize=(9, 5), gridspec_kw={'bottom': 0.15, 'left': 0.15})
clevel = 50
cs = ax2.contourf(X, Y, Z2, levels=clevel)

y_label = r'dw (nm)'
x_label = r'period (nm)'
z_label = r'theta (degree)'

cbar2 = fig2.colorbar(cs)
ticklabs = cbar2.ax.get_yticklabels()
cbar2.ax.set_yticklabels(ticklabs, fontsize=14)
cbar2.ax.set_ylabel(z_label, fontsize=14)

ax2.set_ylabel(x_label, fontsize=14)
ax2.set_xlabel(y_label, fontsize=14)

fig3, ax3 = plt.subplots(figsize=(9, 5), gridspec_kw={'bottom': 0.15, 'left': 0.15})
clevel = 50
cs = ax3.contourf(X, Y, Z3, levels=clevel)

y_label = r'dw (nm)'
x_label = r'period (nm)'
z_label = r'theta (degree)'

cbar3 = fig3.colorbar(cs)
ticklabs = cbar3.ax.get_yticklabels()
cbar3.ax.set_yticklabels(ticklabs, fontsize=14)
cbar3.ax.set_ylabel(z_label, fontsize=14)

ax3.set_ylabel(x_label, fontsize=14)
ax3.set_xlabel(y_label, fontsize=14)

plt.show()

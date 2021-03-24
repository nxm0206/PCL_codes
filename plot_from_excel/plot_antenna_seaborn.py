import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import seaborn as sns

file_loc = "D:/GitFolder/PCL_codes/simulation.xlsx"
df = pd.read_excel(file_loc, sheet_name='Sheet1')
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


selected = []
theta_1d = np.arcsin(neff_1d - 1550 / period_1d) * 180 / np.pi
beta_1d = 10 * np.log10((1 - t10_1d) / (10 * period_1d * 10 ** (-3)))
angle_range = [8.0, 10.0]
# print(theta_1d)
for i in range(len(theta_1d)):
    if theta_1d[i] >= angle_range[0] and theta_1d[i] < angle_range[1]:
        selected.append('Yes')
    else:
        selected.append('No')

antenna_data = {'period(nm)': period_1d, 'dw(nm)': dw_1d, 'neff': neff_1d,'t10': t10_1d,'angle': angle_1d, r'angle $\in$ '+str(angle_range): selected}
df = pd.DataFrame(antenna_data)

sns.set_context("talk", font_scale=1.1)
sns.set(style="ticks",color_codes=True)
size_order = ['Yes', 'No']
fig0, ax0 = plt.subplots(figsize=(9, 6), gridspec_kw={'bottom': 0.15, 'left': 0.15})
sns.scatterplot(ax=ax0, x='dw(nm)', y='period(nm)', hue='angle', size=r'angle $\in$ '+str(angle_range), size_order=size_order, palette="viridis", legend='brief', data=df)
ax0.legend(loc=2)
plt.show()
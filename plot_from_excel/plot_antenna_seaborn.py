import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import seaborn as sns

# import data from Excels
file_loc = "D:/GitFolder/PCL_codes/simulation.xlsx"
# file_loc = "C:/Users/Nie/Desktop/Git Folder/code/simulation.xlsx"
df = pd.read_excel(file_loc, sheet_name='Sheet2')
N_dw_excel = 316
dw = df.iloc[0:N_dw_excel-1, 1].values * 10 ** 9
ddw = dw[1]-dw[0]
N_excel = 532
period_1d = df.iloc[0:N_excel-1, 0].values * 10 ** 9
dw_1d = df.iloc[0:N_excel-1, 1].values * 10 ** 9
neff_1d = df.iloc[0:N_excel-1, 2].values
t_1d = df.iloc[0:N_excel-1, 3].values
angle_1d = df.iloc[0:N_excel-1, 4].values
nperiod_1d = df.iloc[0:N_excel-1, 5].values
# beta_1d = 10 * np.log10((1 - t_1d) / (10 * period_1d * 10 ** (-3)))
for i in range(len(t_1d)):
    if t_1d[i] >= 1.0:
        t_1d[i] = 0.9999

#build pandas Dataframe

theta_1d = np.arcsin(neff_1d - 1550 / period_1d) * 180 / np.pi
beta_1d = 10 * np.log10((1 - t_1d**2) / (nperiod_1d * period_1d * 10 ** (-3)))
angle_range = [9.0, 11.0]
selected = []
for i in range(len(theta_1d)):
    if angle_1d[i] >= angle_range[0] and angle_1d[i] < angle_range[1]:
        selected.append('Yes')
    else:
        selected.append('No')

antenna_data = {'period(nm)': period_1d, 'dw(nm)': dw_1d, 'neff': neff_1d, 't': t_1d, 'angle': angle_1d, r'angle $\in$ '+str(angle_range): selected, 'Perturbation(dB/$\mu m$)': beta_1d}
df = pd.DataFrame(antenna_data)

selected_df = df.loc[df[r'angle $\in$ '+str(angle_range)] == 'Yes']
print(selected_df)
print(df.loc[345])


# fit data
x_beta = selected_df.loc[:,'Perturbation(dB/$\mu m$)'].values
y_dw = selected_df.loc[:,'dw(nm)'].values
# print(beta)
def dw_beta(x, a, b, c, d, e):
    y = a/x +b*x + c*np.exp(d*x) + e
    return y

popt, _ = curve_fit(dw_beta, x_beta, y_dw)
# dw_beta = np.poly1d(dw_beta_fit)
print(popt)
a, b, c, d, e = popt


x_beta_fit = np.arange(np.min(x_beta), np.max(x_beta), 0.01)
y_dw_fit = dw_beta(x_beta_fit, a, b, c, d, e)
# print(len(x_beta_fit))
# print(len(y_dw_fit))





# plot with seaborn
sns.set_context("talk", font_scale=1.0)
sns.set_style('darkgrid')
size_order = ['Yes', 'No']
fig0, ax0 = plt.subplots(figsize=(12, 8), gridspec_kw={'bottom': 0.15, 'left': 0.15})
sns.scatterplot(ax=ax0, x='dw(nm)', y='period(nm)', hue='angle', size=r'angle $\in$ '+str(angle_range), size_order=size_order, palette="viridis", legend='brief', data=df)
# sns.regplot(ax=ax0, x='dw(nm)', y='period(nm)', hue='Perturbation(dB/$\mu m$)', order=3, data=selected_df)
sns.scatterplot(ax=ax0, x='dw(nm)', y='period(nm)', hue='Perturbation(dB/$\mu m$)', marker = 'o', legend='brief', data=selected_df)
ax0.legend(loc=2)
fig1, ax1 = plt.subplots(figsize=(12, 8), gridspec_kw={'bottom': 0.15, 'left': 0.15})
sns.scatterplot(ax=ax1, y='dw(nm)', size='angle', x='Perturbation(dB/$\mu m$)', marker = 'o', legend='brief', data=selected_df)
sns.lineplot(ax=ax1, y=y_dw_fit, x=x_beta_fit)
plt.show()
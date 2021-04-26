import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import seaborn as sns

# import data from Excels
file_loc = "D:/GitFolder/PCL_codes/DataToPlot/SideEtchWGA_simulation.xlsx"
# file_loc = "C:/Users/Nie/Desktop/Git Folder/code/simulation.xlsx"
df = pd.read_excel(file_loc, sheet_name='Sheet2', convert_float=False)
df['period(nm)'] = df['period(nm)'].values* 1e9
df['dw(nm)'] = df['dw(nm)'].values* 1e9
beta2 = 10 * np.log10((-np.log(df['T2'].values)) / (2.0 * df['period(nm)'].values * 1e-3))
beta5 = 10 * np.log10((-np.log(df['T5'].values)) / (5.0 * df['period(nm)'].values * 1e-3))
beta10 = 10 * np.log10((-np.log(df['T'].values)) / (df['Np'].values * df['period(nm)'].values * 1e-3))
print(beta10)
df['emission rate(dB/$\mu m$)'] = beta5
theta = df['theta'].values






angle_range = [9.6, 10.4]
selected = []
for i in range(len(theta)):
    if theta[i] >= angle_range[0] and theta[i] < angle_range[1]:
        selected.append('Yes')
    else:
        selected.append('No')

df['angle $\in$ '+str(angle_range)] = selected

print(df)

selected_df = df.loc[df[r'angle $\in$ '+str(angle_range)] == 'Yes']
# print(selected_df)
# print(df.loc[345])


# fit p_dw
x_dw = selected_df.loc[:,'dw(nm)'].values
y_period = selected_df.loc[:,'period(nm)'].values


p_dw_fit = np.polyfit(x_dw, y_period, 3)
p_dw = np.poly1d(p_dw_fit)
x_dw_fit = np.arange(np.min(x_dw), np.max(x_dw), 0.01)
y_period_fit = p_dw(x_dw_fit)
print("----------------------------------------")
print("p_dw function:")
print(p_dw)
print("----------------------------------------")


# fit dw_beta
x_beta = selected_df.loc[:,'emission rate(dB/$\mu m$)'].values
y_dw = selected_df.loc[:,'dw(nm)'].values
# print(beta)

def dw_beta(x, a, b, c, d , e, f):
    y = a*x**4 + b*x**3 + c*x**2 + d*x + e*np.exp(x) + f
    return y


popt, _ = curve_fit(dw_beta, x_beta, y_dw)
# dw_beta = np.poly1d(dw_beta_fit)
print("----------------------------------------")
print("dw_beta function (a*x**4 + b*x**3 + c*x**2 + d*x + e*np.exp(x) + f) \n parameters [a, b, c, d, f]:")
print(popt)
print("----------------------------------------")
a, b, c, d, e, f = popt


x_beta_fit = np.arange(np.min(x_beta), np.max(x_beta), 0.01)
y_dw_fit = dw_beta(x_beta_fit, a, b, c, d, e, f)






# plot with seaborn
sns.set_context("talk", font_scale=1.0)
sns.set_style('darkgrid')
size_order = ['Yes', 'No']
fig0, ax0 = plt.subplots(figsize=(12, 8), gridspec_kw={'bottom': 0.15, 'left': 0.15})
sns.scatterplot(ax=ax0, x='dw(nm)', y='period(nm)', hue='emission rate(dB/$\mu m$)', size=r'angle $\in$ '+str(angle_range), size_order=size_order, palette="viridis", legend='brief', data=df)
# sns.scatterplot(ax=ax0, x='dw(nm)', y='period(nm)', size='theta', marker = '+', legend='brief', data=selected_df)
sns.lineplot(ax=ax0, y=y_period_fit, x=x_dw_fit)
ax0.legend(loc=2)
fig0, ax1 = plt.subplots(figsize=(12, 8), gridspec_kw={'bottom': 0.15, 'left': 0.15})
sns.scatterplot(ax=ax1, x='dw(nm)', y='period(nm)', hue='theta', size=r'angle $\in$ '+str(angle_range), size_order=size_order, palette="viridis", legend='brief', data=df)
# sns.scatterplot(ax=ax1, x='dw(nm)', y='period(nm)', size='theta', marker = '+', legend='brief', data=selected_df)
sns.lineplot(ax=ax1, y=y_period_fit, x=x_dw_fit)
ax1.legend(loc=2)
fig1, ax2 = plt.subplots(figsize=(12, 8), gridspec_kw={'bottom': 0.15, 'left': 0.15})
sns.scatterplot(ax=ax2, y='dw(nm)', size='theta', x='emission rate(dB/$\mu m$)', marker = 'o', legend='brief', data=selected_df)
sns.lineplot(ax=ax2, y=y_dw_fit, x=x_beta_fit)
plt.show()
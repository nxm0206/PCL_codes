import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_loc = "D:/GitFolder/PCL_codes/DataToPlot/SideEtchWGA_simulation.xlsx"
df = pd.read_excel(file_loc, sheet_name='Sheet3', convert_float=False)
# print(df)
period = df['period'].values*1e9
angle = df['angle'].values

p_angle_fit = np.polyfit(angle, period, 3)
p_angle = np.poly1d(p_angle_fit)
x_angle_fit = np.arange(np.min(angle), np.max(angle), 0.01)
y_period_fit = p_angle(x_angle_fit)
print(p_angle)
print(p_angle(10))
fig, ax = plt.subplots(figsize=(12,5),gridspec_kw={'hspace': 0.8, 'bottom': 0.2})

ax.plot(angle, period, 'o', label='simulated')
ax.plot(x_angle_fit, y_period_fit , '-', label='fitted')
# ax.set_ylim(0.2, 1.2)
# ax.plot(wav, 0.886*wav/1000/126.5*180/np.pi, label='simulation')
# ax.legend(fontsize=12)
ax.set_ylabel(r'period(nm)', fontsize=14)
ax.set_xlabel(r'angle', fontsize=14)
plt.show()
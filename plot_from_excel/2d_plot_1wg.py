import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker, cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
from numpy import ma


wg = 0.01
wwg = 0.5
hwg = 0.22
hs = 0.07
# ws = 3

file_loc = "D:/simulation/SOI_antenna/field/one_wg.xlsx"
df = pd.read_excel(file_loc, sheet_name='g10',dtype=float)
y = np.asarray(df.iloc[1:212,0].values*10**6)
z = np.asarray(df.iloc[214:262,0].values*10**6)

y_g = np.where(((y < wwg/2.0+wg) & (y >= wwg/2.0)) | ((y < -wwg/2.0) & (y >= -wwg/2.0-wg)), 1, 0)
z_g = np.where((z < hwg) & (z >= 0), 1, 0)
X_g, Y_g = np.meshgrid(z_g, y_g)


X, Y = np.meshgrid(z, y)



E = np.asarray(df.iloc[264:475,0:48].values)
print(np.sum(X_g*Y_g*E)/np.sum(E))
print(np.sum(E))

E = 10*np.log10(E)
# E = ma.masked_where(E <= 0, E)
# plt.imshow(E, cmap = 'autumn' , interpolation = 'nearest' )
# print(type(E))
#
#
fig, ax = plt.subplots(figsize=(9,5), gridspec_kw={'bottom': 0.15, 'left': 0.15})
clevel = 30
cs = ax.contourf(Y, X, E, levels=clevel)


x_label = r'$x (\mu{}m)$'
y_label = r'$y (\mu{}m)$'
z_label = r'Normalized intensity (log scale, a.u.)'
ax.set_xlabel(x_label, fontsize=14)
ax.set_ylabel(y_label, fontsize=14)
ax.tick_params(axis='both', which='major', labelsize=14)



# Add a color bar which maps values to colors.
# cbar=fig.colorbar(surf, shrink=0.5, aspect=5)
# cbar.ax.set_ylabel(z_label, fontsize=14)
cbar = fig.colorbar(cs)
ticklabs = cbar.ax.get_yticklabels()
cbar.ax.set_yticklabels(ticklabs, fontsize=14)
cbar.ax.set_ylabel(z_label, fontsize=14)





plt.plot([-wwg/2.0, -wwg/2.0, wwg/2.0, wwg/2.0, -wwg/2.0],
         [0, hwg, hwg, 0, 0], 'red', lw=3)

plt.plot([-wg-wwg/2.0, -wg-wwg/2.0, -wwg/2.0, -wwg/2.0, -wg-wwg/2.0],
         [0, hwg, hwg, 0, 0], 'black', ls="--")

plt.plot([wg+wwg/2.0, wg+wwg/2.0, wwg/2.0, wwg/2.0, wg+wwg/2.0],
         [0, hwg, hwg, 0, 0], 'black', ls="--")

plt.show()
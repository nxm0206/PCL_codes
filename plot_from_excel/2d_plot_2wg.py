import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker, cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
from numpy import ma

gap = 0.6
wg = 0.2
wwg = 0.5
hwg = 0.22
hs = 0.07
ws = 3

file_loc = "D:/simulation/SOI_antenna/field/two_wgs.xlsx"
df = pd.read_excel(file_loc, sheet_name='gap600',dtype=float)
y = np.asarray(df.iloc[1:206,0].values*10**6)
z = np.asarray(df.iloc[208:255,0].values*10**6)

y_g = np.where((y < wg/2.0) & (y >= -wg/2.0), 1, 0)
z_g = np.where((z < hwg) & (z >= hs), 1, 0)
X_g, Y_g = np.meshgrid(z_g, y_g)


X, Y = np.meshgrid(z, y)



E = np.asarray(df.iloc[257:462,0:47].values)

dn2 = 3.48**2-1**2
neff = 2.491339
wav = 1.55
integration = np.sum(X_g*Y_g*E*E*dn2)/np.sum(E*E)
kappa = np.pi/neff/wav*integration
print("kappa = ", kappa)
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





plt.plot([-ws/2.0, -ws/2.0, -wg/2.0-gap-wwg, -wg/2.0-gap-wwg,
         -wg/2.0-gap,-wg/2.0-gap,wg/2.0+gap,wg/2.0+gap,wg/2.0+gap+wwg,
          wg/2.0+gap+wwg,ws/2.0,ws/2.0, -ws/2.0],
         [0, hs, hs, hwg, hwg, hs, hs, hwg, hwg, hs, hs, 0, 0], 'red', lw=3)

plt.plot([-wg/2.0, -wg/2.0, wg/2.0, wg/2.0, -wg/2.0],
         [hs,hwg,hwg,hs,hs],'black', ls="--")

plt.show()
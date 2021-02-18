from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np


fig = plt.figure()
ax = fig.gca(projection='3d')

# Make data.
X = np.arange(-np.pi, np.pi, 0.1)
Y = np.arange(-np.pi, np.pi, 0.1)
X, Y = np.meshgrid(X, Y)
Z = 1/4.0*(2+np.sin(X)+np.sqrt(3)*np.cos(X)*np.cos(Y))

# Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.Blues,
                       linewidth=0, antialiased=False)

x_label = r'$\theta(rad)$'
y_label = r'$\varphi(rad)$'
z_label = r' '
# Customize the z axis.
# ax.set_zlim(-1.01, 1.01)
ax.set_xlabel(x_label, fontsize=14)
ax.set_ylabel(y_label, fontsize=14)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))


# Add a color bar which maps values to colors.
cbar=fig.colorbar(surf, shrink=0.5, aspect=5)
cbar.ax.set_ylabel(z_label, fontsize=14)
plt.show()
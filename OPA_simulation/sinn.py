import numpy as np
import matplotlib.pyplot as plt


theta = np.linspace(-np.pi, np.pi, 20000)
N=100
k=2*np.pi/1.55
d=2
alpha = 0
f = np.sin(N*(k*d*np.cos(theta) + alpha)/2.0) / np.sin((k*d*np.cos(theta) + alpha)/2.0)

plt.plot(theta,f)
plt.show()
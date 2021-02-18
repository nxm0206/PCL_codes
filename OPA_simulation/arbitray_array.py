import numpy as np
import matplotlib.pyplot as plt
import scipy.special as ssl

N = 1000
phi = np.linspace(-np.pi, np.pi, N)
dphi = phi[1] - phi[0]
F = np.zeros_like(phi)

dx = 0.5
L = 64
array_position = np.linspace(-(L/2-1)*dx-dx/2.0, (L/2-1)*dx+dx/2.0, L)
# print(array_position)
wav = 1.55
k0 = 2*np.pi/wav
Al = 1
alphal = 0
In_array = np.ones_like(array_position)*Al*np.exp(1j*alphal*np.ones_like(array_position))
M = 1000
m_array = np.linspace(-M, M, 2*M+1)
# print(m_array)

for phi_i in range(len(phi)):
    LHS = np.zeros_like(array_position)
    print(phi_i)
    for i in range(len(array_position)):
        Jn_array = ssl.jn(m_array, k0*array_position[i])*np.exp(-1j*m_array*phi[phi_i])
        LHS[i] = In_array[i]*np.sum(Jn_array)

    F[phi_i] = sum(LHS)


# Jn_array = ssl.jn(1, k0*array_position)
# print(Jn_array)
plt.plot(phi*180/np.pi,abs(F))
plt.show()

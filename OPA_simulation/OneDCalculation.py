import numpy as np
import matplotlib.pyplot as plt
import random


def array_factor(xn, varphin, An, wav, resolution):
    k = 2.0*np.pi/wav
    phi = np.linspace(-np.pi/2.0, np.pi/2.0, resolution)
    Etot = np.zeros_like(phi)
    for i in range(len(phi)):
        Etot[i] = abs(np.sum(An*np.exp(1j*(k*xn*np.sin(phi[i])+varphin))))

    return phi, Etot


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    N = 32

    array = np.linspace(0, N-1, N)
    xn = array*2
    An = np.ones_like(array)
    varphin = np.pi*array*(0.0)

    # xn = np.asarray([0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 62])
    # rand = np.random.rand(17)*4-2
    # rand[0] = 0
    # rand[-1] = 0
    # xn = xn+rand

    An = np.asarray([0.1, 0.2, 0.7, 0.8, 0.9, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5])
    An = An*len(An)/np.sum(An)
    # An = np.ones_like(xn)
    # varphin = np.zeros_like(xn)

    print(xn)
    resolution = 10000
    wav = 1.55
    phi, E = array_factor(xn, varphin, An, wav, resolution)
    phi = phi * 180 / np.pi
    normalized_E = abs(E)/np.max(abs(E))
    normalized_E_log = 10*np.log10(normalized_E)
    zeorpoints = np.min(normalized_E)

    fig, ax = plt.subplots(figsize=(12,4), gridspec_kw={'bottom': 0.15, 'left': 0.15})
    # fig, ax = plt.subplots(figsize=(9, 5), gridspec_kw={'bottom': 0.15, 'left': 0.15})
    ax.plot(phi*180/np.pi,normalized_E,'-')
    x_label = r'$\phi (\circ)$'
    y_label = r'Normalized AF'
    # z_label = r''
    ax.set_xlabel(x_label, fontsize=14)
    ax.set_ylabel(y_label, fontsize=14)
    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.tick_params(axis='both', which='minor', bottom='on')
    # ax.set_ylim([-40, 5])
    # ax.set_xlim([-25, 25])
    # plt.plot(xn)
    plt.show()

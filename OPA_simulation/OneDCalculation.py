import numpy as np
import matplotlib.pyplot as plt
import random
from scipy import signal


def array_factor(xn, varphin, An, wav, resolution):
    k = 2.0*np.pi/wav
    phi = np.linspace(-np.pi/2.0, np.pi/2.0, resolution)
    Etot = np.zeros_like(phi)
    for i in range(len(phi)):
        Etot[i] = abs(np.sum(An*np.exp(1j*(k*xn*np.sin(phi[i])+varphin))))

    return phi* 180 / np.pi, abs(Etot)/np.max(abs(Etot))

def array_plot(x,y):

    fig, ax = plt.subplots(figsize=(12, 4), gridspec_kw={'bottom': 0.15, 'left': 0.15})
    # fig, ax = plt.subplots(figsize=(9, 5), gridspec_kw={'bottom': 0.15, 'left': 0.15})
    ax.plot(x, y, '-')
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
    # plt.show()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    N = 100
    gap = 2.0
    array_equal = np.linspace(0, N-1, N)
    xn_equal = array_equal*gap
    An_equal = np.ones_like(array_equal)
    varphin_equal = np.pi*array_equal*(0.0)

    N_sparse = 100
    # average_gap = 200.0/N_sparse
    xn_sparse = np.linspace(start=0.0, stop=500.0, num=N_sparse, endpoint=True)
    rand = np.random.rand(len(xn_sparse))*4-2
    rand[0] = 0
    rand[-1] = 0
    # xn = xn+rand
    xn_sparse = np.around(xn_sparse+rand, decimals=1)
    print(xn_sparse)



    # An = np.asarray([0.1, 0.2, 0.7, 0.8, 0.9, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5])
    # An = An*len(An)/np.sum(An)
    An_sparse = np.ones_like(xn_sparse)
    varphin_sparse = np.zeros_like(xn_sparse)

    # print(xn)
    resolution = 10000
    wav = 1.55
    phi_equal, E_equal = array_factor(xn_equal, varphin_equal, An_equal, wav, resolution)
    phi_sparse, E_sparse = array_factor(xn_sparse, varphin_sparse, An_sparse, wav, resolution)
    E_equal_log = 10*np.log10(E_equal)
    E_sparse_log = 10 * np.log10(E_sparse)

    num_peak = signal.find_peaks(-E_sparse, distance=1)
    phi_minimuns = phi_sparse[num_peak[0]]
    E_minimuns = E_sparse[num_peak[0]]
    print(np.min(abs(phi_minimuns)))
    # zeorpoints = np.min(normalized_E)

    # array_plot(phi_equal, E_equal_log)
    array_plot(phi_sparse, E_sparse)
    for ii in range(len(num_peak[0])):
        plt.plot(phi_sparse[num_peak[0][ii]], E_sparse[num_peak[0][ii]], '*', markersize=10)
    plt.show()


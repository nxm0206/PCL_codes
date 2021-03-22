import numpy as np
import matplotlib.pyplot as plt
import random
from scipy import signal


def array_factor(xn, varphin, An, wav, resolution):
    k = 2.0*np.pi/wav
    phi = np.linspace(-np.pi/2.0, np.pi/2.0, resolution)
    Ptot = np.zeros_like(phi)
    for index in range(len(phi)):
        Ptot[index] = abs(np.sum(An*np.exp(1j*(k*xn*np.sin(phi[index])+varphin))))**2

    return phi * 180 / np.pi, Ptot/np.max(Ptot)

def array_plot(x,y):

    fig, ax = plt.subplots(figsize=(12, 4), gridspec_kw={'bottom': 0.15, 'top': 0.99, 'left': 0.08, 'right': 0.99})
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

def sparse_array_sidepeak(p_sparse, phi_sparse):
    num_peak = signal.find_peaks(p_sparse, height=[0, 0.9], distance=1)
    # phi_peaks = phi_sparse[num_peak[0]]
    peaks = p_sparse[num_peak[0]]
    max_peak_index = np.argmax(peaks)
    max_peak_angle = phi_sparse[num_peak[0][max_peak_index]]
    max_peak_power = p_sparse[num_peak[0][max_peak_index]]
    return max_peak_angle, max_peak_power

if __name__ == '__main__':

    # define equal-gap array with random number
    N = 128
    gap = 2.0
    array_equal = np.linspace(0, N-1, N)
    xn_equal = array_equal*gap
    An_equal = np.ones_like(array_equal)
    varphin_equal = np.pi*array_equal*0.0
    resolution = 10000
    wav = 1.55

    # define sparse array
    N_sparse = 32
    ArraySize = 256.0
    average_gap = ArraySize/N_sparse
    xn_sparse = np.zeros(N_sparse)
    min_gap = 4.0
    xn_sparse[-1] = ArraySize
    for i in range(int(N_sparse/2-1)):
        xn_sparse[i+1] = xn_sparse[i]+(min_gap + np.random.rand() * (average_gap-min_gap)*2.0)
    for i in range(int(N_sparse/2-1)):
        xn_sparse[N_sparse-i-2] = xn_sparse[N_sparse-i-1]-(min_gap + np.random.rand() * (average_gap-min_gap)*2.0)
    xn_sparse = np.around(xn_sparse, decimals=1)

    # define sparse array by specifying positions
    xn_sparse = [0.0, 6.5, 14.6, 24.8, 36.0, 46.4, 54.8, 62.1, 70.6, 82.3, 89.8, 101.4, 111.9, 121.0, 125.0, 131.5, 135.5, 140.3, 144.4, 153.3, 165.2, 171.8, 183.5, 189.5, 195.0, 202.7, 212.4, 222.1, 228.0, 235.3, 244.7, 256.0]
    # xn_sparse = np.asarray([0, 4, 9, 15, 22, 30, 39, 49,60,72,85,99,114,130,147,165])*wav

    dx=[]
    for i in range(len(xn_sparse)-1):
        dx.append(xn_sparse[i+1]-xn_sparse[i])
    print("minimum gap: "+str(np.min(dx)))
    print("average gap: "+str(np.mean(dx)))

    xn_sparse = np.asarray(xn_sparse)
    print(xn_sparse)


    An_sparse = np.ones_like(xn_sparse)
    varphin_sparse = np.zeros_like(xn_sparse)

    # print(xn)

    phi_equal, p_equal = array_factor(xn_equal, varphin_equal, An_equal, wav, resolution)
    phi_sparse, p_sparse = array_factor(xn_sparse, varphin_sparse, An_sparse, wav, resolution)
    P_equal_log = 10*np.log10(p_equal)
    P_sparse_log = 10 * np.log10(p_sparse)

    # array_plot(phi_equal, p_equal)
    array_plot(phi_sparse, p_sparse)
    # plt.ylim([-14,0])
    min_gap = [(-10, 10)]


    max_peak_angle, max_peak_power = sparse_array_sidepeak(p_sparse, phi_sparse)
    print("max peak height: "+str(max_peak_power))
    # plt.plot(max_peak_angle, max_peak_power, 'o', markersize=10)



    plt.show()


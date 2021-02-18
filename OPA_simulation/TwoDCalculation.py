import numpy as np
import matplotlib.pyplot as plt


def array_factor(xn, varphin, An, wav, resolution):
    k = 2.0*np.pi/wav
    phi = np.linspace(-np.pi/2.0, np.pi/2.0, resolution)
    Etot = np.zeros_like(phi)
    for i in range(len(phi)):
        Etot[i] = np.sum(An*np.exp(1j*(k*xn*np.sin(phi[i])+varphin)))

    return phi, Etot


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    N = 64

    array = np.linspace(0, N-1, N)
    xn = array*1.0
    varphin = xn*np.pi*0
    An = np.ones_like(array)

    # xn = np.asarray([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30])
    # varphin = np.zeros_like(xn)
    # An = np.ones_like(xn)


    print(xn)
    resolution = 10000
    wav = 0.532
    phi, E = array_factor(xn, varphin, An, wav, resolution)
    normalized_E = abs(E)/np.max(abs(E))
    normalized_E_log = 10*np.log10(normalized_E)

    fig, ax = plt.subplots(figsize=(9,5), gridspec_kw={'bottom': 0.15, 'left': 0.15})
    ax.plot(phi*180/np.pi,normalized_E,'-')
    x_label = r'$方向角\phi (\circ)$'
    y_label = r'阵列因子'
    # z_label = r''
    ax.set_xlabel(x_label, fontsize=14)
    ax.set_ylabel(y_label, fontsize=14)
    ax.tick_params(axis='both', which='major', labelsize=14)
    # ax.set_ylim([0, 1.2])
    ax.set_xlim([-40, 40])
    # plt.plot(xn)
    plt.show()

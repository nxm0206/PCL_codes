import numpy as np
import matplotlib.pylab as plt

def AllPass(wav, radius, r, a, neff0, ng0, lambda0):

    dneff = (neff0-ng0)/lambda0
    neff = neff0+dneff*(wav-lambda0)
    phi = 2*np.pi*neff/wav*(2*np.pi*radius*10**3)
    T = (a ** 2 - 2 * r * a * np.cos(phi) + r ** 2) / (1 - 2 * a * r * np.cos(phi) + (r * a) ** 2)
    return T

def AddDrop(wav, radius, r1, r2, a, neff0, ng0, lambda0):

    dneff = (neff0-ng0)/lambda0
    neff = neff0+dneff*(wav-lambda0)
    phi = 2*np.pi*neff/wav*(2*np.pi*radius*10**3)
    Tp = ((r2 * a) ** 2 - 2 * r1 * r2 * a * np.cos(phi) + r1 ** 2) / (1 - 2 * a * r1 * r2 * np.cos(phi) + (r1 * r2 * a) ** 2)
    Td = (1 - r1 ** 2) * (1 - r2 ** 2) * a / (1 - 2 * a * r1 * r2 * np.cos(phi) + (r1 * r2 * a) ** 2)
    return Tp, Td

def AddDropFWHM(r1, r2, a, ng0, lambda0, radius):
    FWHM = (1 - r1 * r2 * a) * lambda0 / (np.pi * ng0 * 2 * np.pi * radius * 1000 * np.sqrt(r1 * r2 * a)) * 1000
    return FWHM

def AddDropER(r1, r2, a):
    Tp_min = ((r2 * a) ** 2 - 2 * r1 * r2 * a + r1 ** 2) / (1 - 2 * a * r1 * r2 + (r1 * r2 * a) ** 2)
    Tp_max = ((r2 * a) ** 2 + 2 * r1 * r2 * a + r1 ** 2) / (1 + 2 * a * r1 * r2 + (r1 * r2 * a) ** 2)
    Td_min = (1 - r1 ** 2) * (1 - r2 ** 2) * a / (1 + 2 * a * r1 * r2 + (r1 * r2 * a) ** 2)
    Td_max = (1 - r1 ** 2) * (1 - r2 ** 2) * a / (1 - 2 * a * r1 * r2 + (r1 * r2 * a) ** 2)

    return Tp_max, Tp_min, Td_max, Td_min

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    wav = np.linspace(1530, 1570, 20001)
    Tp, Td = AddDrop(wav, 10, r1=np.sqrt(1-0.1**2), r2=np.sqrt(1-0.1**2), a=0.991, neff0=2.31, ng0=4.23, lambda0=1550)
    Tp_max, Tp_min, Td_max, Td_min = AddDropER(r1=0.7, r2=0.7, a=0.996)
    print("Tp_max: " + str(Tp_max))
    print("Tp_min: " + str(Tp_min))
    print("Td_max: " + str(Td_max))
    print("Td_min: " + str(Td_min))



    x_label = "wavelength (nm)"
    y_label = "transmission"
    fig, (ax1, ax2) = plt.subplots(2, gridspec_kw={'hspace': 0.4, 'wspace': 0})
    ax1.plot(wav, Tp, 'r')
    ax1.set_xlabel(x_label, fontsize=15)
    ax1.set_ylabel(y_label, fontsize=15)
    ax2.plot(wav, Td, 'g')
    ax2.set_xlabel(x_label, fontsize=15)
    ax2.set_ylabel(y_label, fontsize=15)

    r = np.linspace(0.6, 0.999, 401)
    FWHM = AddDropFWHM(r, r, 0.996, 4.23, 1550, 9)
    Tp_max, Tp_min, Td_max, Td_min = AddDropER(r, r, 0.996)
    ER = -10*np.log10(Td_max/Td_min)

    fig, ax3 = plt.subplots(1,gridspec_kw={'hspace': 0.4, 'wspace': 0, "right": 0.85})
    ax3.plot(r, FWHM, "r")
    ax3.set_xlabel("r", fontsize=15)
    ax3.set_ylabel("FWHM (nm)", fontsize=15)

    ax4 = ax3.twinx()
    ax4.plot(r, ER, "g")
    ax4.set_ylabel("ER (dB)", fontsize=15)
    plt.show()

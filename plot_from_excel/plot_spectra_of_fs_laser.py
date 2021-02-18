import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_loc = "D:/measurement_data/20201218/spectrum_vs_fiber_length.xlsx"
df = pd.read_excel(file_loc, sheet_name='spectra')
wav = df.iloc[2:1503,0].values
I_00m = df.iloc[2:1503,1].values
I_01m = df.iloc[2:1503,4].values
I_04m = df.iloc[2:1503,7].values
I_07m = df.iloc[2:1503,10].values
I_10m = df.iloc[2:1503,13].values
I_13m = df.iloc[2:1503,16].values
I_16m = df.iloc[2:1503,19].values

# fig, (ax1, ax2) = plt.subplots(1, 2)
fig, axs = plt.subplots(7, sharex=True, sharey=True, figsize=(6, 10), gridspec_kw={'hspace': 0.2, 'bottom': 0.05, 'top': 0.99})
# fig, ax1 = plt.subplots(1, figsize=(6, 8), gridspec_kw={'hspace': 0.2, 'bottom': 0.1, 'top': 0.95})

axs[0].plot(wav, I_00m, label='0 m')
axs[1].plot(wav, I_01m, label='1 m')
axs[2].plot(wav, I_04m, label='4 m')
axs[3].plot(wav, I_07m, label='7 m')
axs[4].plot(wav, I_10m, label='10 m')
axs[5].plot(wav, I_13m, label='13 m')
axs[6].plot(wav, I_16m, label='16 m')
for ax in axs:
    ax.legend(fontsize=14)

# ax2.plot(wav, I_04m, '-', label='measurement')
# ax3.plot(wav, I_07m, '-', label='measurement')
# ax4.plot(wav, I_10m, '-', label='measurement')
# ax5.plot(wav, I_13m, '-', label='measurement')
# # ax6.plot(wav, I_16m, '-', label='measurement')

# ax.set_ylim(0.2, 1.2)
# ax.plot(wav, 0.886*wav/1000/126.5*180/np.pi, label='simulation')
# ax.legend(fontsize=12)
axs[3].set_ylabel(r'spectral intensity (dBm)', fontsize=12)
axs[6].set_xlabel(r'wavelength(nm)', fontsize=12)
plt.show()
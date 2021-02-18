import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_loc = "D:/measurement_data/20201130/calculation.xlsx"
df = pd.read_excel(file_loc, sheet_name='Sheet2')
wav = df.iloc[0:201,0].values
eff = df.iloc[0:201,2].values*100.0

fig, ax = plt.subplots(figsize=(6,2.5),gridspec_kw={'hspace': 0.8, 'bottom': 0.2})

ax.plot(wav, eff, '-', label='measurement')
# ax.set_ylim(0.2, 1.2)
# ax.plot(wav, 0.886*wav/1000/126.5*180/np.pi, label='simulation')
# ax.legend(fontsize=12)
ax.set_ylabel(r'overall efficiency (%)', fontsize=12)
ax.set_xlabel(r'wavelength(nm)', fontsize=12)
plt.show()
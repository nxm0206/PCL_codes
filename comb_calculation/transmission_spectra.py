import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import interpolate as interp
from scipy.signal import find_peaks
from dispersion_calculation import FSR_nm_GHz_percm_cal

data = pd.read_excel('D:\仿真\lumerical_mode\dispersion\dispersion_460.xlsx', sheet_name = 'WG340X300')
# data = pd.read_excel('D:\仿真\lumerical_mode\dispersion\dispersion_532.xlsx', sheet_name = 'WG400X300')
# data = pd.read_excel('D:\仿真\lumerical_mode\dispersion\dispersion_850.xlsx', sheet_name = 'WG800X300')
# data = pd.read_excel('D:\仿真\lumerical_mode\dispersion\dispersion_1550.xlsx', sheet_name = 'WG2000X300')

wav = data.iloc[5:24, 0].values.astype(float)

neff_TE1 = data.iloc[5:24, 1].values.astype(float)
neff_TE2 = data.iloc[5:24, 11].values.astype(float)
print(neff_TE1[1])
print(neff_TE2[1])

ng_TE1 = data.iloc[5:24, 4].values.astype(float)
ng_TE2 = data.iloc[5:24, 14].values.astype(float)


r1 = 0.95
a1 = 0.95
L = 0.7*10**3
c = 3*10**8*10**6

FSR1 = FSR_nm_GHz_percm_cal(wav,ng_TE1,L)
FSR2 = FSR_nm_GHz_percm_cal(wav,ng_TE2,L)
print(np.mean(FSR1[0]),np.mean(FSR1[1]))
print(np.mean(FSR2[0]),np.mean(FSR2[1]))

phi_TE1 = 2*np.pi*neff_TE1/wav*L
phi_TE2 = 2*np.pi*neff_TE2/wav*L

n_points=10000001
f1 = interp.interp1d(wav, phi_TE1)
f2 = interp.interp1d(wav, phi_TE2)

wav_start = 0.44
wav_stop = 0.49

# wav_start = wav[0]+0.01
# wav_stop = wav[-1]-0.01

wav_interp = np.linspace(wav_start,wav_stop,num=n_points,endpoint=True)

phi_TE1_interp = f1(wav_interp)
phi_TE2_interp = f2(wav_interp)
f_interp = c/wav_interp/10**9



def trans_allpass(r, a, phi):
    return (a**2-2*r*a*np.cos(phi)+r**2)/(1-2*a*r*np.cos(phi)+r**2*a**2)


T1 = trans_allpass(r1, a1, phi_TE1_interp)
T2 = trans_allpass(r1, a1, phi_TE2_interp)

peaks1, _ = find_peaks(-T1, height=-0.90)
peaks2, _ = find_peaks(-T2, height=-0.90)
index1_coupling=[]
index2_coupling=[]
df_coupling=[]

df_tolerance = 1
for peaks in peaks1:
    df_peak = abs(f_interp[peaks] - f_interp[peaks2])
    # print(df_peak)
    if df_peak.min() <= df_tolerance:
        df_coupling.append(round(df_peak.min(),3))
        # print(np.argmin(df_peak))
        index1_coupling.append(np.where(peaks1 == peaks)[0][0])
        index2_coupling.append(np.argmin(df_peak))

# print(index1_coupling)
# print(index2_coupling)
# print(df_coupling)
# print(wav_interp[peaks2[index2_coupling]])
diff_index = np.diff(index1_coupling)
index1_seg = []
index2_seg = []
df_seg = []
seg_start = 0
if np.mean(diff_index) == 1:
    index1_seg.append(index1_coupling)
    index2_seg.append(index2_coupling)
    df_seg.append(df_coupling)

else:
    for i in range(len(diff_index)):
        if diff_index[i] > 1.0:
            index1_seg.append(index1_coupling[seg_start:i+1])
            index2_seg.append(index2_coupling[seg_start:i + 1])
            df_seg.append(df_coupling[seg_start:i+1])
            seg_start = i+1


# print(index1_seg)
# print(index2_seg)
# print(df_seg)

i = 0
df_coupling_final = []
index1_coupling_final = []
index2_coupling_final = []
for seg in index1_seg:
    if len(seg) > 1:
        df_coupling_final.append(min(df_seg[i]))
        index1_coupling_final.append(seg[np.argmin(df_seg[i])])
        index2_coupling_final.append(index2_seg[i][np.argmin(df_seg[i])])
    else:
        df_coupling_final.append(df_seg[i][0])
        index1_coupling_final.append(index1_seg[i][0])
        index2_coupling_final.append(index2_seg[i][0])
    i = i+1

print(df_coupling_final)
print(index1_coupling_final)
print(index2_coupling_final)
print(wav_interp[peaks2[index2_coupling_final]].round(3))


plt.plot(wav_interp[peaks1[index1_coupling_final]], T1[peaks1[index1_coupling_final]], "o")
plt.plot(wav_interp[peaks2[index2_coupling_final]], T2[peaks2[index2_coupling_final]], "x")


# plt.plot(c/wav_interp/10**9, 10*np.log10(T1))
# plt.plot(c/wav_interp/10**9, 10*np.log10(T2))
plt.plot(wav_interp, T1, "green")
plt.plot(wav_interp, T2, "red")
# plt.plot(c/wav_interp/10**9, T2)
plt.xlabel('wavelength(um)')
plt.ylabel('transmission')

plt.show()
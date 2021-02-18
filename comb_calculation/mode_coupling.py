import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import interpolate as interp
from scipy.signal import find_peaks
from dispersion_calculation import FSR_nm_GHz_percm_cal

# data = pd.read_excel('D:\科研资料\仿真\lumerical_mode\dispersion\dispersion_460.xlsx', sheet_name = 'WG380X300')
data = pd.read_excel('D:\科研资料\仿真\lumerical_mode\dispersion\dispersion_850.xlsx', sheet_name = 'WG800X300')
# data = pd.read_excel('D:\科研资料\仿真\lumerical_mode\dispersion\dispersion_1550.xlsx', sheet_name = 'WG2000X300')

# load wavelength list
wav = data.iloc[5:54, 0].values.astype(float)
# load neff list of the two modes
neff_TE1 = data.iloc[5:54, 1].values.astype(float)
neff_TE2 = data.iloc[5:54, 11].values.astype(float)
# print(neff_TE1[1])
# print(neff_TE2[1])
# load ng list of the two modes
ng_TE1 = data.iloc[5:54, 4].values.astype(float)
ng_TE2 = data.iloc[5:54, 14].values.astype(float)

#simulation wavelength range
wav_start = 0.849
wav_stop = 0.856
offset = 0

# wavelength list of n_points
n_points=200000001
wav_interp = np.linspace(wav_start,wav_stop,num=n_points,endpoint=True)
# interp as function of wavelength
wav_ng1 = interp.interp1d(wav, ng_TE1)
wav_ng2 = interp.interp1d(wav, ng_TE2)
wav_n1 = interp.interp1d(wav, neff_TE1)
wav_n2 = interp.interp1d(wav, neff_TE2)

# interpolated lists
n_TE1_interp = wav_n1(wav_interp)
n_TE2_interp = wav_n2(wav_interp)
ng_TE1_interp = wav_ng1(wav_interp)
ng_TE2_interp = wav_ng2(wav_interp)




# calculate the native resonance frequencies of two modes
r1 = 0.95
a1 = 0.95
L = 2.5*10**3
c = 3*10**8*10**6
def trans_allpass(r, a, phi):
    return (a**2-2*r*a*np.cos(phi)+r**2)/(1-2*a*r*np.cos(phi)+r**2*a**2)

# calculate native FSR of two modes
phi_TE1_interp = 2*np.pi*n_TE1_interp/wav_interp*L
phi_TE2_interp = 2*np.pi*n_TE2_interp/wav_interp*L
FSR1 = FSR_nm_GHz_percm_cal(wav_interp,ng_TE1_interp,L)
FSR2 = FSR_nm_GHz_percm_cal(wav_interp,ng_TE2_interp,L)
print(np.mean(FSR1[1]))
print(np.mean(FSR2[1]))

T1 = trans_allpass(r1, a1, phi_TE1_interp)
T2 = trans_allpass(r1, a1, phi_TE2_interp)

peaks1, _ = find_peaks(-T1, height=-0.90)
peaks2, _ = find_peaks(-T2, height=-0.90)

# frequency list of n_points
f_interp = c/wav_interp/10**9
# interp as function of frequency
fn1 = interp.interp1d(f_interp,n_TE1_interp)
fn2 = interp.interp1d(f_interp,n_TE2_interp)
fng1 = interp.interp1d(f_interp,ng_TE1_interp)
fng2 = interp.interp1d(f_interp,ng_TE2_interp)

res1 = f_interp[peaks1]
res2 = f_interp[peaks2]


# calculate mode coupling induced res shifts

kappa21 = 8.25*1j
kappa12 = -8.25*1j
tau_o1 = 2.79
tau_e1 = 4.0
tau_o2 = 0.578
tau_e2 = 3.38

fn_points = 50000001
shifted_res = []
T_res_list = []
# print(c/res1[50]/10**9)
# res_couple = 795
# res_range = 40
# res_min, res_max = int(res_couple-res_range/2), int(res_couple+res_range/2)
start_res = 1
stop_res = len(res1)-2
for i in range(start_res,stop_res):
    print(i)
    f = np.linspace(res1[i]-50, res1[i]+50, num=fn_points, endpoint=True)
    delta_1 = res1[i]-f
    delta_2 = res2[i+offset]-f

    E1 = (1j*kappa21*np.sqrt(2/tau_e1)+(1/tau_o1+1/tau_e1+1j*delta_1)*np.sqrt(2/tau_e2))/((1/tau_o1+1/tau_e1+1j*delta_1)*(1/tau_o2+1/tau_e2+1j*delta_2)+kappa12*kappa21)
    E2 = (1j*kappa12*np.sqrt(2/tau_e2)+(1/tau_o2+1/tau_e2+1j*delta_2)*np.sqrt(2/tau_e1))/((1/tau_o1+1/tau_e1+1j*delta_1)*(1/tau_o2+1/tau_e2+1j*delta_2)+kappa12*kappa21)
    T_res = abs(1-E1*np.sqrt(2/tau_e1)-E2*np.sqrt(2/tau_e2))**2

    peaks_T, _ = find_peaks(-T_res, height=-0.90)
    # print(peaks_T)
    shifted_res.append(f[peaks_T[0]])
    T_res_list.append(T_res)
    # plt.plot(delta_1, T_res)

# x=delta_1
# y=np.linspace(start_res, stop_res, num=stop_res-start_res+1, endpoint=True)
# z=np.asarray(T_res_list)
#
# fig1, (ax0) = plt.subplots(nrows=1)
#
# im = ax0.pcolormesh(x, y, z)
# ax0.set_xlabel('relative resonance frequency (GHz)')
# ax0.set_ylabel('resonance number')
# cbar = fig1.colorbar(im, ax=ax0)
# cbar.set_label('Transmission')


beta2=[]
D2=[]
D_wav=[]
for i in range(1, len(shifted_res)-1):
    FSR_res = FSR_nm_GHz_percm_cal(c/shifted_res[i]/10**9, fng1(shifted_res[i]), L)
    D2.append(-shifted_res[i+1]-shifted_res[i-1]+2*shifted_res[i])
    beta2.append(-fn1(shifted_res[i])*2*np.pi*(-shifted_res[i+1]-shifted_res[i-1]+2*shifted_res[i])/(2.0*np.pi*FSR_res[1])**2)
    D_wav.append(c/shifted_res[i]/10**9)
D_couple = -2*np.pi/np.asarray(D_wav)**2*np.asarray(beta2)*10**9



d_D_couple = abs(np.diff(D_couple))
print(D_couple)
factor = 1.3
for i in range(3, len(D_couple)-3):
    print(D_couple[i])
    print((np.mean(D_couple[i-3])+np.mean(D_couple[i+3])))
    if D_couple[i] >= (D_couple[i-3]+D_couple[i+3])/2.0*factor:
        print(D_couple[i])
        D_couple[i] = np.mean([D_couple[i-3], D_couple[i+3]])

fig2, (ax1) = plt.subplots(nrows=1)
ax1.plot(D_wav, D_couple,'-')
ax1.set_xlabel('wavelength(um)')
ax1.set_ylabel('Dispersion(ps/km/nm)')
plt.show()



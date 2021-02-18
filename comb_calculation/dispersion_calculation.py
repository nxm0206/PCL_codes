import numpy as np


def FSR_nm_GHz_percm_cal(lam_um, ng, L_um):
    c = 3*10**8
    lam = lam_um * 10 ** -6
    L = L_um * 10 ** -6
    FSR_in_wavelegnth=lam*lam/ng/L
    FSR_in_frequency=c*FSR_in_wavelegnth/lam/lam
    FSR_in_wavenumber=FSR_in_wavelegnth/lam/lam
    return [FSR_in_wavelegnth*10**9, FSR_in_frequency*10**-9, FSR_in_wavenumber*10**-2]


def L_mm_cal(lam_in_nm, ng, FSR_in_GHz):
    c = 3*10**8
    return c/ng/FSR_in_GHz/10**9*1000


# print(FSR_nm_GHz_percm_cal(1.550, 1.774, 5.92*10**3))
# print(FSR_nm_GHz_percm_cal(1.550, 1.738, 5.92*10**3))
# print(L_mm_cal(1550, 1.774, 75))
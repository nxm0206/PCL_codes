import pyvisa as visa
import numpy as np
import time
import pandas as pd
# import seaborn as sns
import matplotlib.pylab as plt
from datetime import datetime


def read_power(powermeter, unit):
    if unit == "dBm":
        powermeter.write('SENSe:CHANnel:POWer:UNIT 0')
        power = float("{:.8f}".format(float(powermeter.query('read1:pow?'))))
        print("measured power: ", power, "dBm")
    elif unit == "mW":
        powermeter.write('SENSe:CHANnel:POWer:UNIT 1')
        power =  float("{:.8f}".format(float(powermeter.query('read1:pow?'))*1e6))
        print("measured power: ", power, 'mW')
    else:
        print('Error: wrong settings')
        power = 0
    return power

def TL_set_wav(TunableLaser,wav):
    TunableLaser.write('sour0:wav ' + str(wav) + 'NM')
    print("set wavelength to: "+ str(wav)+" nm")

def TL_set_pow(TunableLaser,p):
    TunableLaser.write('sour0:pow ' + str(p) + 'DBM')
    print("set laser power to: " + str(p) +" dBm")


if __name__ == '__main__':
    rm = visa.ResourceManager()
    powermeter = rm.open_resource('USB0::0x0957::0x3718::DE53500169::0::INSTR')
    TunableLaser = rm.open_resource('GPIB0::20::INSTR')
    print("loading instrument: ", powermeter.query('*IDN?'))
    print("loading instrument: ", TunableLaser.query('*IDN?'))
    print("Finished.")


    wav_start = 1450.0
    wav_stop = 1650.0
    wav_step = 1.0

    wav_list = np.linspace(wav_start, wav_stop, int((wav_stop-wav_start)/wav_step+1))
    power = 0.0 #dbm
    unit = 'dBm'
    data_to_CSV = []

    for i in range(len(wav_list)):
        wav = wav_list[i]
        pow = power
        TL_set_wav(TunableLaser, wav)
        TL_set_pow(TunableLaser, pow)
        time.sleep(.300)
        measured_power = read_power(powermeter,unit)
        data_to_CSV.append({'wavelength(nm)': wav, 'set_power('+unit+')': pow, 'measured_power('+unit+')': measured_power})
        df = pd.DataFrame(data_to_CSV)


    now = datetime.now()
    dt_string = now.strftime("%Y%m%d_%H%M")

    df.to_csv(dt_string+"wavelength_scan.csv",index=False)

    x = df.loc[:, 'wavelength(nm)'].values
    y1 = df.loc[:, 'set_power('+unit+')'].values
    y2 = df.loc[:, 'measured_power('+unit+')'].values

    fig0, ax0 = plt.subplots(figsize=(12, 8), gridspec_kw={'bottom': 0.15, 'left': 0.15})
    ax0.plot(x, y1, '-o', label = 'TL set power')
    ax0.plot(x, y2, '-o', label = 'measured power')
    ax0.set_xlabel('wavelength (nm)', fontsize=20)
    ax0.set_ylabel('power (dBm)', fontsize=20)
    ax0.tick_params(axis='both', which='major', labelsize=18)
    ax0.grid(c='k', ls='-', alpha=0.1)
    plt.legend(fontsize=18)
    plt.savefig("WavelengthScan_"+dt_string+".png")
    plt.show()


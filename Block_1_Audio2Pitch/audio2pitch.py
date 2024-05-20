import sys
import csv
import matplotlib.pyplot as plt
import numpy as np
from playsound import playsound

from scipy.signal import get_window
sys.path.append("PSPM/")
import dftModel as DFT
import utilFunctions as UF
import harmonicModel as HM
import stft


################################################################
#HOW TO USE THIS CODE:
#Right after executing enter 1, 2 or 3 in the terminal.
#1: For melodies with a fundemental frequency between 120 and 500 Hz.
#2: For melodies with a fundemental frequency between 500 and 1000 Hz.
#3: Diferent type of window with different paramenters. (Usage and parameters still in work)
#OUTPUT:
#The script displays the histogram of the sound with the fundemental frequency highlited in a black line.
#The fundemental frequency is also stored in a .cvs file.
################################################################


if __name__ == '__main__':
    input_file = 'sounds/flute-A4.wav'
    #playsound('sounds/cello-double-2.wav')
        
    selected = int(input())

    if selected == 1:       #Normal option
        window = 'hamming'
        M = 8000
        N = 8192
        f0et = 10
        t = -55
        minf0 = 120
        maxf0 = 500
    elif selected == 2:     #High frequency option
        window = 'hamming'
        M = 8000
        N = 8192
        f0et = 10
        t = -55
        minf0 = 500
        maxf0 = 1000
    elif selected == 3:     #Secondary option (still in prossess)
        window = 'blackman'
        M = 16000
        N = 16384
        f0et = 10
        t = -33
        minf0 = 120
        maxf0 = 300


    H = 256 
    fs, x = UF.wavread(input_file) 
    w  = get_window(window, M)   
    f0 = HM.f0Detection(x, fs, w, N, H, t, minf0, maxf0, f0et) 

    filename = 'f0.csv'

    np.savetxt(filename, f0, delimiter=',', fmt='%s')

    maxplotfreq = 500.0    
    fig = plt.figure(figsize=(15, 9))

    mX, pX = stft.stftAnal(x, w, N, H) 
    mX = np.transpose(mX[:,:int(N*(maxplotfreq/fs))+1])
        
    timeStamps = np.arange(mX.shape[1])*H/float(fs)                             
    binFreqs = np.arange(mX.shape[0])*fs/float(N)
        
    plt.pcolormesh(timeStamps, binFreqs, mX, shading='auto')
    plt.plot(timeStamps, f0, color = 'k', linewidth=1.5)
        
    plt.ylabel('Frequency (Hz)')
    plt.xlabel('Time (s)')
    plt.legend(('f0',))
    plt.show()

    

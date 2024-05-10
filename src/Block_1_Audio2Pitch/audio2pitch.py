import sys
import matplotlib.pyplot as plt
import numpy as np

from scipy.signal import get_window
sys.path.append("PSPM/")
import dftModel as DFT
import utilFunctions as UF
import harmonicModel as HM
import stft


if __name__ == '__main__':
    input_file = 'sounds/cello-double-2.wav'
        
    ### Change these analysis parameter values marked as XX

    window = 'hamming'
    M = 8000
    N = 8192
    f0et = 10
    t = -55
    minf0 = 120
    maxf0 = 200


    # No need to modify the code below, just understand it
    H = 256 
    fs, x = UF.wavread(input_file) 
    w  = get_window(window, M)   
    f0 = HM.f0Detection(x, fs, w, N, H, t, minf0, maxf0, f0et) 




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

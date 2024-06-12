import os
import sys
import csv
import matplotlib.pyplot as plt
import numpy as np
import librosa as li

from scipy.signal import get_window
sys.path.append('src/Block_1_Audio2Pitch/PSPM/')
import dftModel as DFT
import utilFunctions as UF
import harmonicModel as HM
import stft

from scipy.signal import get_window, medfilt
from scipy.ndimage import gaussian_filter1d

################################################################
#HOW TO USE THIS CODE:
#Right after executing, write the name of the audio file you want to use.
#After that, enter 1, 2, 3 or 4 in the terminal.
#1: For melodies with a fundemental frequency between 120 and 500 Hz.
#2: For human voice audios:
#### After selecting human voices, select the pitch of the audio:
#### 1: low frequencies (80-500 Hz)
#### 2: high frequencies (500-1000 Hz)
#3: For instruments audio:
#### 1: low frequencies (80-500 Hz)
#### 2: medium frequencies (500-1000 Hz)
#### 3: high frequencies (1000-10000 Hz)
#4: Custom option: you can select the pitch range you want.
#OUTPUT:
#The script displays the histogram of the sound with the fundemental frequency highlited in a black line.
#The fundemental frequency is also stored in a .cvs file.
################################################################

def get_user_input(prompt, valid_options):
    while True:
        try:
            selected = int(input(prompt))
            if selected in valid_options:
                return selected
            else:
                print(f"Invalid option. Please select one of the following: {valid_options}")
        except ValueError:
            print("Invalid input. Please enter a number.")

def audio2Pitch(audioName, flag=1):
    dataset_dir = 'tests/Datasets/'
    nameSplit = audioName.split(".")
    if nameSplit[-1] == 'wav':
        input_file = dataset_dir + audioName
    else:
        input_file = dataset_dir + audioName+'.wav'
        
    selected = get_user_input("Select input audio type, [1] normal, [2] high freq., [3] in progress, [4] Custom: ", [1, 2, 3, 4])

    if selected == 1:       #Normal option
        window, M, N, f0et, t, minf0, maxf0 = 'hamming', 8000, 8192, 10, -55, 120, 500
    elif selected == 2:     #High frequency option
        window, M, N, f0et, t = 'blackman', 8000, 8192, 10, -55
        selected = get_user_input("Select pitch range [1] for 80-500Hz, [2] for 500-1000Hz): ", [1, 2])
        if selected == 1:
            minf0 = 80
            maxf0 = 500
        elif selected == 2:
            minf0 = 500
            maxf0 = 1000
    elif selected == 3:     #Secondary option (still in prossess)
        window, M, N, f0et, t, minf0, maxf0 = 'hamming', 8000, 8192, 10, -55, 120, 500
        selected = get_user_input("Select pitch range, [1] for 80-500Hz, [2] for 500-1000Hz, [3] for 1000-10000Hz): ", [1, 2, 3])
        if selected == 1:
            minf0 = 80
            maxf0 = 500
        elif selected == 2:
            minf0 = 500
            maxf0 = 1000
        elif selected == 3:
            minf0 = 1000
            maxf0 = 10000
    elif selected == 4:     # Custom option
        window, M, N, f0et, t = 'blackman', 8000, 8192, 10, -55
        minf0 = int(input("Select min pitch range: "))
        maxf0 = int(input("Select max pitch range: "))


    H = 256 
    x, fs = li.load(input_file)
    bpm, _ = li.beat.beat_track(y=x, sr=fs)

    M = N
    w  = get_window(window, M)
    
    if flag == 1:
        # Display the spectrogram with selected frequency range
        plot_spectrogram(x, fs, H, N, w, audioName, minf0, maxf0)
    
    adjust_freqs = input("Would you like to adjust the frequency range? (y/n): ")
    if adjust_freqs.lower() == 'y':
        minf0 = int(input("Enter new minimum pitch range: "))
        maxf0 = int(input("Enter new maximum pitch range: "))
    
    f0 = HM.f0Detection(x, fs, w, N, H, t, minf0, maxf0, f0et) 
    
    
    # Smooth the f0 track using a median filter
    f0 = medfilt(f0, kernel_size=5)
    # Further smooth using Gaussian filter
    f0 = gaussian_filter1d(f0, sigma=2)
    

    maxplotfreq = maxf0    
    fig = plt.figure(figsize=(13, 7))

    mX, pX = stft.stftAnal(x, w, N, H) 
    mX = np.transpose(mX[:, :int(N * (maxplotfreq / fs)) + 1])
        
    timeStamps = np.arange(mX.shape[1]) * H / float(fs)                             
    binFreqs = np.arange(mX.shape[0]) * fs / float(N)    
    
    if timeStamps.shape[0] > f0.shape[0]:
        # Discard the last entries in timeStamps
        timeStamps = timeStamps[:f0.shape[0]]
        mX = mX[:len(binFreqs), :len(timeStamps)]
    elif timeStamps.shape[0] < f0.shape[0]:
        # Discard the last entries in f0
        f0 = f0[:timeStamps.shape[0]]
        
    # Combine timestamps and f0 values into one array
    output_dir = f'src/outputs/f0_{audioName}.csv'
    output_data = np.column_stack((timeStamps, f0))
    np.savetxt(output_dir, output_data, delimiter=',', fmt='%s')
    
    if flag == 1:
        plt.pcolormesh(timeStamps, binFreqs, mX, shading='auto')
        plt.plot(timeStamps, f0, color = 'k', linewidth=1.5)
            
        plt.ylabel('Frequency (Hz)')
        plt.xlabel('Time (s)')
        plt.legend(('f0',))
        plt.show()

    return H, bpm, selected, output_data


def plot_spectrogram(x, fs, H, N, w, audioName, minf0=None, maxf0=None):
    D = li.stft(x, n_fft=N, hop_length=H, window=w)
    S_db = li.amplitude_to_db(np.abs(D), ref=np.max)

    plt.figure(figsize=(14, 5))
    li.display.specshow(S_db, sr=fs, hop_length=H, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title(f'Spectrogram of {audioName} Audio')

    if minf0 is not None and maxf0 is not None:
        plt.axhline(y=minf0, color='r', linestyle='-', linewidth=1.5)
        plt.axhline(y=maxf0, color='r', linestyle='-', linewidth=1.5)
        plt.text(0, minf0 + 20, f'Min F0: {minf0} Hz', color='r', fontsize=10)
        plt.text(0, maxf0 + 20, f'Max F0: {maxf0} Hz', color='r', fontsize=10)

    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.show()
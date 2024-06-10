import numpy as np
import librosa

def yin_pitch_tracking(audio_path, sr=22050, frame_length=2048, hop_length=512, fmin=50.0, fmax=2000.0):
    """
    Detect pitch using the YIN algorithm.

    Parameters:
    - audio_path (str): Path to the audio file.
    - sr (int): Sampling rate for loading the audio.
    - frame_length (int): Length of the frames for analysis.
    - hop_length (int): Number of samples between successive frames.
    - fmin (float): Minimum frequency to consider for pitch detection.
    - fmax (float): Maximum frequency to consider for pitch detection.

    Returns:
    - pitches (np.ndarray): Array of detected pitches (frequencies in Hz).
    - times (np.ndarray): Array of corresponding time stamps.
    """
    # Load the audio file
    y, sr = librosa.load(audio_path, sr=sr)
    
    # Use the YIN algorithm to extract pitch
    pitches = librosa.yin(y, fmin=fmin, fmax=fmax, sr=sr, frame_length=frame_length, hop_length=hop_length)
    
    # Calculate the time stamps
    times = librosa.frames_to_time(np.arange(len(pitches)), sr=sr, hop_length=hop_length)
    
    # Estimate the tempo
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr, hop_length=hop_length)

    return pitches, times, tempo
    
def store_results_csv(pitches, times, output_path= 'src/outputs/f0.csv'):
    output_data = np.column_stack((times, pitches))
    np.savetxt(output_path, output_data, delimiter=',', fmt='%s')
    
    # # Print the detected pitches and their corresponding times
    # for t, p in zip(times, pitches):
    #     print(f"Time: {t:.4f}s, Pitch: {p:.2f}Hz")

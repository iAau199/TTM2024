import librosa
import numpy as np

# Define a function to perform audio to pitch conversion
def audio_to_pitch(audio_file):
    # Load the audio file
    y, sr = librosa.load(audio_file)
    
    # Extract pitch using librosa's pitch detection function
    pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)
    
    # Convert pitches to Hz
    pitches_hz = [librosa.hz_to_midi(p) for p in pitches]
    
    return pitches_hz

# Define a function to calculate Mean Absolute Error (MAE)
def calculate_mae(predictions, ground_truth):
    mae = np.mean(np.abs(predictions - ground_truth))
    return mae

# Test the audio to pitch conversion
def test_audio_to_pitch_conversion():
    # Test audio file
    audio_file = 'test_audio.wav'
    
    # Ground truth pitches (in MIDI note numbers)
    ground_truth_pitches = [60, 62, 64, 67, 69]  # Example pitches
    
    # Perform audio to pitch conversion
    predicted_pitches = audio_to_pitch(audio_file)
    
    # Calculate Mean Absolute Error (MAE)
    mae = calculate_mae(predicted_pitches, ground_truth_pitches)
    
    # Check if MAE is within acceptable range
    tolerance = 1  # Set tolerance for acceptable error
    if mae <= tolerance:
        print("Audio to pitch conversion is correct.")
    else:
        print("Audio to pitch conversion is incorrect.")
        print(f"Mean Absolute Error: {mae}")

# Run the test
test_audio_to_pitch_conversion()

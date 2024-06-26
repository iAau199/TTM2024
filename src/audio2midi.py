from Block_1_Audio2Pitch import audio2pitch as a2p
from Block_2_Pitch2MIDI import pitch2midi as p2m


if __name__ == "__main__":
    audioName = input("Enter the name of the audio file: ")
    H, tempo, selected, time_f0 = a2p.audio2Pitch(audioName)
    
    print("tempo:", tempo)
    print("H:", H)
    sampling_rate = 44100
  
    p2m.pitch2midi(H, tempo, sampling_rate, time_f0, audioName)
    
def audio2midi(audioName, flag=1):
    H, tempo, selected, time_f0 = a2p.audio2Pitch(audioName, flag)
    sampling_rate = 44100
    p2m.pitch2midi(H, tempo, sampling_rate, time_f0, audioName)
    return audioName, H, tempo, sampling_rate
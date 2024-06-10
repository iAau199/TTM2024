from Block_1_Audio2Pitch import audio2pitch_copy as a2p
from Block_2_Pitch2MIDI import pitch2midi_copy as p2m


if __name__ == "__main__":
  # audio2pitch
  audio_file = "src/Block_1_Audio2Pitch/sounds/01-AchGottundHerr_slow_violin.wav"
  pitches, times, tempo = a2p.yin_pitch_tracking(audio_file)
  print("tempo:",tempo)
  output_path = 'src/outputs/f0.csv'
  a2p.store_results_csv(pitches, times, output_path)
  
  # pitch2midi
  tempo_microseconds_per_beat = int((60 * 1000000) / tempo[0])
  output_midi_path = 'src/outputs/output.mid'
  p2m.pitches_to_midi(pitches, times, output_midi_path, tempo_microseconds_per_beat)
from Block_1_Audio2Pitch import audio2pitch as a2p
from Block_2_Pitch2MIDI import pitch2midi as p2m


if __name__ == "__main__":
  #CALL AUDIO2PITCH FUNCTIONS --> WE NEED CSV, TEMPO, HOP_SIZE
  H, tempo = a2p.audiotopitch()
  
  print(tempo)

  sampling_rate = 44100

  pitch_signal = p2m.csv_to_array("f0.csv")
  midi_notes = p2m.detect_midi_notes(pitch_signal)
  note_toggles = p2m.detect_note_toggles(midi_notes)
  note_times = p2m.detect_note_times(pitch_signal, H, sampling_rate)
  midi_conversion = p2m.create_array(midi_notes, note_toggles, note_times)
  p2m.save_to_midi(midi_conversion, tempo)
  
  # H, tempo = a2p.audiotopitch()

  # sampling_rate = 44100
  # p2m.pitch2midi(H, tempo, sampling_rate)
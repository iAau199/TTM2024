import librosa
import mido
from mido import MidiFile, MidiTrack, Message
import csv



def csv_to_array(filename):
  pitch_array = []

  with open(filename, mode='r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
      float_row = [float(item) for item in row]
      pitch_array.extend(float_row)
  return pitch_array

def detect_midi_notes(pitch_signal):
  

  notes = []
  midi_notes = []

  for pitch in pitch_signal:
    if pitch > 0:
      note = librosa.hz_to_note(pitch)
      midi_note = librosa.note_to_midi(note)
      midi_notes.append(midi_note)
    else:
      midi_notes.append(0)

  return midi_notes

def detect_midi_notes(pitch_signal):
  notes = []
  midi_notes = []

  for pitch in pitch_signal:
    if pitch > 0:
      note = librosa.hz_to_note(pitch)
      midi_note = librosa.note_to_midi(note)
      midi_notes.append(midi_note)
    else:
      midi_notes.append(0)

  return midi_notes

def detect_note_toggles(pitch_signal):
    note_toggles = []
    start = 0

    for i in range(1, len(pitch_signal)):
        prev_note = pitch_signal[i - 1]
        current_note = pitch_signal[i]
        if prev_note != current_note:
            note_toggles.append((start, i))
            start = i

    note_toggles.append((start, len(pitch_signal) - 1))

    return note_toggles

def detect_note_times(pitch_array, hop_size, sampling_rate):
  
  frame_ids = list(range(len(pitch_array)))
  timestamps = [(frame_id * hop_size) / sampling_rate for frame_id in frame_ids]
  return timestamps

def create_array(midi_notes, toggles, time):
    note_times = []

    for toggle in toggles:
        start_index, end_index = toggle
        start_time = time[start_index]
        end_time = time[end_index]
        note_times.append((start_time, end_time, midi_notes[start_index]))

    return note_times

def save_to_midi(midi_conversion, tempo, filename = "output.mid"):
  mid = MidiFile()
  track = MidiTrack()
  mid.tracks.append(track)

  tempo = int(tempo[0])

  track.append(mido.MetaMessage('set_tempo', tempo=tempo))

  for start_time, end_time, note_pitch in midi_conversion:
    ticks_per_beat = 480
    previous_end_time_ticks = 0

    start_time_ticks = mido.second2tick(start_time, ticks_per_beat, tempo)
    end_time_ticks = mido.second2tick(end_time, ticks_per_beat, tempo)

    delta_time_on = start_time_ticks - previous_end_time_ticks
    delta_time_off = end_time_ticks - start_time_ticks

    note_on = Message('note_on', note = note_pitch, time = int(delta_time_on))
    note_off = Message('note_off', note = note_pitch, time = int(delta_time_off))

    track.append(note_on)
    track.append(note_off)

    previous_end_time_ticks = end_time_ticks

  mid.save(filename)

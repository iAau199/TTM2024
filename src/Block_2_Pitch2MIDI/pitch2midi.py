import librosa
import mido
from mido import MidiFile, MidiTrack, Message
import csv

output_dir = 'src/outputs/'

def csv_to_array(filename):
  pitch_array = []

  with open(filename, mode='r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
      float_row = [float(item) for item in row]
      pitch_array.extend(float_row)
  return pitch_array

def detect_midi_notes(pitch_signal):
  midi_notes = []

  for pitch in pitch_signal:
    if pitch > 0:
      note = librosa.hz_to_note(pitch)
      midi_note = librosa.note_to_midi(note)
      midi_notes.append(midi_note)
    else:
      midi_notes.append(0)
  print("midi_notes:", midi_notes)
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
    
    filtered_toggles = [toggle for toggle in note_toggles if toggle[1] - toggle[0] > 3]
    
    print("note_toggles:", filtered_toggles)
    return filtered_toggles

def detect_note_times(pitch_array, hop_size, sampling_rate):
  frame_ids = list(range(len(pitch_array)))
  timestamps = [(frame_id * hop_size) / sampling_rate for frame_id in frame_ids]
  return timestamps

def create_array(midi_notes, toggles, time):
    note_times = []

    for toggle in toggles:
        start_index, end_index = toggle
        midle_idx = start_index + round((end_index - start_index)/2)
        start_time = time[start_index]
        end_time = time[end_index]
        note_times.append((start_time, end_time, midi_notes[midle_idx]))
    print("note_times:", note_times)
    return note_times

def increase_volume(input_file, output_file, volume_factor):
    mid = mido.MidiFile(input_file)
    for i, track in enumerate(mid.tracks):
        for msg in track:
            if msg.type == 'note_on':
                # Increase the velocity by the volume factor, but cap it at 127 (MIDI max value)
                msg.velocity = min(127, int(msg.velocity * volume_factor))
    mid.save(output_file)

def save_to_midi(midi_conversion, tempo, filename=output_dir + 'output.mid'):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    # Convert tempo to microseconds per beat
    tempo_us_per_beat = int(mido.bpm2tempo(tempo[0]))

    # Set tempo in the MIDI file
    track.append(mido.MetaMessage('set_tempo', tempo=tempo_us_per_beat))

    previous_end_time_ticks = 0

    for start_time, end_time, note_pitch in midi_conversion:
        ticks_per_beat = mid.ticks_per_beat

        # Convert start and end times to ticks
        start_time_ticks = int(mido.second2tick(start_time, ticks_per_beat, tempo_us_per_beat))
        end_time_ticks = int(mido.second2tick(end_time, ticks_per_beat, tempo_us_per_beat))

        # Calculate the delta times for note_on and note_off events
        delta_time_on = start_time_ticks - previous_end_time_ticks
        delta_time_off = end_time_ticks - start_time_ticks

        # Create note_on and note_off messages
        note_on = Message('note_on', note=note_pitch, time=int(delta_time_on))
        note_off = Message('note_off', note=note_pitch, time=int(delta_time_off))

        # Append messages to the track
        track.append(note_on)
        track.append(note_off)

        # Update previous end time
        previous_end_time_ticks = end_time_ticks

    # Save MIDI file
    mid.save(filename)

def pitch2midi(H, tempo, sampling_rate, time_f0, audio_name):
    pitch_signal = time_f0[:, 1]
    timestamps = time_f0[:, 0]
    midi_notes = detect_midi_notes(pitch_signal)
    note_toggles = detect_note_toggles(midi_notes)
    note_times = detect_note_times(pitch_signal, H, sampling_rate)
    midi_conversion = create_array(midi_notes, note_toggles, timestamps)
    filename = output_dir + audio_name + '_output.mid'
    save_to_midi(midi_conversion, tempo, filename)
    increase_volume(filename, output_dir + audio_name + '_outputHigh.mid', 10)
    print("Finished pitch2midi.")
    
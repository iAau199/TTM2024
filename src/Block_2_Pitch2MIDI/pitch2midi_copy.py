import numpy as np
import mido
import csv

def frequency_to_midi(frequency):
    """
    Convert a frequency in Hz to a MIDI note number.

    Parameters:
    - frequency (float): Frequency in Hz.

    Returns:
    - midi_note (int): Corresponding MIDI note number.
    """
    if frequency <= 0:
        return None  # Return None for invalid frequencies
    return int(round(69 + 12 * np.log2(frequency / 440.0)))

def pitches_to_midi(pitches, times, output_path, tempo=500000):
    """
    Convert detected pitches to a MIDI file.

    Parameters:
    - pitches (np.ndarray): Array of detected pitches (frequencies in Hz).
    - times (np.ndarray): Array of corresponding time stamps (in seconds).
    - output_path (str): Path to the output MIDI file.
    - tempo (int): Tempo in microseconds per beat (default is 500000, which is 120 BPM).
    """
    # Create a new MIDI file with a single track
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)

    # Set the tempo
    track.append(mido.MetaMessage('set_tempo', tempo=tempo))

    # Initialize the time of the last note
    last_time = 0

    for time, pitch in zip(times, pitches):
        midi_note = frequency_to_midi(pitch)
        if midi_note is not None:
            # Calculate the delta time in ticks
            delta_time = int((time - last_time) * mid.ticks_per_beat * (120 / (tempo / 1000000)))
            last_time = time

            # Add note on and note off messages
            track.append(mido.Message('note_on', note=midi_note, velocity=64, time=delta_time))
            track.append(mido.Message('note_off', note=midi_note, velocity=64, time=delta_time + 1))

    # Save the MIDI file
    mid.save(output_path)
    print(f"Saved MIDI file to: {output_path}")

# This script should read some MIDI file and to extract pitch and note annotations
# with an specific hopsize.
import numpy as np
from pathlib import Path
import numpy as np
from mido import (
    MidiFile,
    MidiTrack,
    MetaMessage,
    Message,
    tick2second,
    bpm2tempo,
    second2tick,
)

TUNING_FREQ = 440 #44100

def midi_note_to_frequency(midi_note: int, tuning: float = TUNING_FREQ) -> float:
    return 2 ** ((midi_note - 69) / 12.0) * tuning

def get_pitch_curve_from_annotations(
    sample_rate: int, hop_size: int, duration: float, annotations: list
) -> np.ndarray:
    # refilling silences
    if not duration:
        duration = annotations[-1][0]
    n_samples = duration * sample_rate
    n_blocks = int(np.ceil(n_samples / hop_size) + 1)
    curve = np.zeros(shape=(n_blocks, 2), dtype=np.float32)
    curve[:, 0] = np.linspace(0, duration, n_blocks)
    # estimate curve index for each time stamp in pitch_anno
    annotations = np.array(annotations)
    idxs = np.round(annotations[:, 0] * sample_rate / hop_size).astype(int)
    # assign pitch values to each array block
    curve[idxs, 1] = annotations[:, 1]
    return curve

def read_midi(midi_path: Path) -> MidiFile:
    return MidiFile(str(midi_path))


def write_midi(
    outpath: Path,
    note_list: list,
    bpm: int = 120,
    ticks_per_beat: int = 96,
    key: str = "C",
    numerator: int = 4,
    denominator: int = 4,
):
    # prepare MIDI file: create file, create track
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    tempo = bpm2tempo(bpm)
    mid.ticks_per_beat = ticks_per_beat

    # define metadata - key_signature, set_tempo, time_signature
    track.append(MetaMessage("key_signature", key=key))
    track.append(MetaMessage("set_tempo", tempo=tempo))
    track.append(
        MetaMessage("time_signature", numerator=numerator, denominator=denominator)
    )

    # convert notes to note_on and note_off message and append messages
    for note in note_list:
        # note_on message
        track.append(
            Message(
                "note_on",
                channel=1,
                note=int(note[2]),
                velocity=127,
                time=int(note[0]),
            )
        )
        # note_off message
        track.append(
            Message(
                "note_off",
                channel=1,
                note=int(note[2]),
                velocity=127,
                time=int(note[1]),
            )
        )

    # add end_of_track meta message
    track.append(MetaMessage("end_of_track"))

    # save the file
    print(f"Writing MIDI file to {bpm} bpm and {tempo} tempo in {outpath}")
    mid.save(outpath)


def get_tempo(mid) -> float:
    for msg in mid:  # Search for tempo
        if msg.type == "set_tempo":
            return msg.tempo
    return 500000  # If not found return default tempo


def get_notes_from_midi(midi_data: MidiFile, bpm: float) -> list:
    # modified version after online_songs metrics failed
    note_list = []
    tempo = bpm2tempo(bpm)
    for track in midi_data.tracks:
        #print('Track {}: {}'.format(i, track.name))
        cumulated_time = 0
        for msg in track:
            if msg.is_meta or msg.type not in ["note_on", "note_off"]:
                continue

            msg_time_sec = tick2second(msg.time, midi_data.ticks_per_beat, tempo)
            # change msg.time to linear time instead of deltas
            cumulated_time += msg_time_sec
            msg.time = cumulated_time

        for n, msg in enumerate(track):
            if msg.type == "note_on":
                # find its note_off and get its time
                off_msg = None
                for _msg in track[n + 1 :]:
                    if _msg.type == "note_off" and _msg.note == msg.note:
                        # found it
                        off_msg = _msg
                        break

                # append a new note
                note_list.append(
                    Note(
                        msg.note,
                        "",
                        None,
                        msg.time,
                        off_msg.time,
                        midi_note_to_frequency(msg.note),
                        msg.velocity,
                        off_msg.velocity,
                    )
                )
    return note_list


def notes_to_pitch_gt(
    samplerate: int,
    hopsize: int,
    note_list: list,
    shift: int = None,
    duration: float = None,
) -> np.ndarray:
    # generate note annotations using <timestamp> <pitch>
    pitch_gt = []
    time_interval = hopsize / samplerate
    for note in note_list:
        # from note.start estimate the closed timestamp for an specific hopsize and sample rate
        nframe = np.ceil(note.start * samplerate / hopsize)
        time_marker = nframe * hopsize / samplerate
        if shift:
            note.midi_note = note.midi_note + shift
            note.pitch = midi_note_to_frequency(note.midi_note)
        # accumulate indexes until the timestamp lower to note.end
        while time_marker <= note.end:
            pitch_gt.append([time_marker, float(note.pitch)])
            time_marker += time_interval
    if not duration:
        duration = pitch_gt[-1][0]
    curve = get_pitch_curve_from_annotations(samplerate, hopsize, duration, pitch_gt)
    return np.array(pitch_gt), curve


def notes_to_note_gt(note_list: list, transposition_value: int = 0) -> np.ndarray:
    # generate note annotations using <onset> <offset> <note>
    note_gt = []
    for note in note_list:
        if note.end - note.start > 0.1:  # force note duration larger than 0.1s
            note_gt.append([note.start, note.end, note.midi_note + transposition_value])
    return np.array(note_gt)


def notes_to_pitches(note_number_list: list):
    return midi_note_to_frequency(np.array(note_number_list))


def midi2pitch(midi_path: Path, sample_rate, hop_size, tempo) -> None:
    # (1) read midi file with mido
    # (2) extract note toggle messages.
    # (3) generate pitch annotations using an specific hopsize: <start-time> <Hz>
    # (4) generate note annotations: <onset> <offset> <midi-number>
      
    # read MIDI file
    mid = read_midi(midi_path)
    # extract a sequence of Notes
    notes_list = get_notes_from_midi(mid, tempo)
    # generate pitch and notes annotations from MIDI file (groundtruth)
    pitch_gt, f0_curve = notes_to_pitch_gt(sample_rate, hop_size, notes_list)
    notes_gt = notes_to_note_gt(notes_list)

    return pitch_gt, f0_curve, notes_gt

class Note:
    def __init__(
        self,
        midi_note,
        root,
        n_octave,
        start=0,
        end=0,
        pitch=0,
        velocity=0,
        ofsset_velocity=0,
    ):
        self.midi_note = midi_note
        self.root = root
        self.n_octave = n_octave
        self.start = start
        self.end = end
        self.duration = self.end - self.start
        self.pitch = pitch
        self.onset_velocity = velocity
        self.offset_velocity = ofsset_velocity

    def __str__(self):
        return f"The MIDI note is {int(self.midi_note)} that starts in {self.start}s and ends in {self.end}s\
            \nwith {self.pitch}Hz of pitch, {self.onset_velocity} of onset velocity and {self.offset_velocity} of offset velocity."

    def __repr__(self, eval: bool = True) -> str:
        if eval:
            return f"Note({self.midi_note}, {self.start}, {self.end}, {self.pitch}, {self.onset_velocity}, {self.offset_velocity})"
        else:
            return f"Note({self.midi_note}, {self.root}, {self.n_octave}, {self.start}, {self.end}, {self.duration}, {self.pitch}, {self.onset_velocity}, {self.offset_velocity})"

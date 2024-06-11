import os
import sys
import unittest
import numpy as np
import mir_eval
import librosa as li
import pretty_midi
from pathlib import Path
import matplotlib.pyplot as plt

# Get the current working directory
script_dir = Path().resolve()

# Add the src directory to the sys.path
SRC_DIR = script_dir / "src"
TESTS_DIR = script_dir / "tests"
print(SRC_DIR)
print(TESTS_DIR)
sys.path.append(str(SRC_DIR))
sys.path.append(str(TESTS_DIR))

# import src.Block_1_Audio2Pitch.audio2pitch as a2p
# import src.Block_2_Pitch2MIDI.pitch2midi as p2m


class TestEndToEnd(unittest.TestCase):
    def setUp(self):
        self.audio_path = TESTS_DIR / 'Datasets/piano.wav'
        self.f0_dir = SRC_DIR / 'outputs/f0_piano.csv'
        self.output_midi_file = SRC_DIR / 'outputs/piano_output.mid'
        self.reference_midi_path = TESTS_DIR / 'Datasets/piano-MIDI.mid'

        self.assertTrue(os.path.exists(self.audio_path), "Test audio file does not exist")
        self.assertTrue(os.path.exists(self.f0_dir), "F0 CSV file does not exist")
        self.assertTrue(os.path.exists(self.output_midi_file), "Output MIDI file does not exist")
        self.assertTrue(os.path.exists(self.reference_midi_path), "Reference MIDI file does not exist")

        self.x, self.fs = li.load(self.audio_path)
        self.f0 = np.loadtxt(self.f0_dir, delimiter=',')
        

    def test_end_to_end(self):
        self.reference_f0, self.ref_f0_curve, self.ref_notes_gt = midi2pitch(Path(self.reference_midi_path))
        print("f0 shape:", self.f0.shape)
        print("reference curve shape:", self.ref_f0_curve.shape)
        #f0_evaluation = mir_eval.melody.evaluate(self.reference_f0[:, 0], self.reference_f0[:, 1], self.f0[:, 0], self.f0[:, 1])
        f0_evaluation = mir_eval.melody.evaluate(self.ref_f0_curve[:, 0], self.ref_f0_curve[:, 1], self.f0[:, 0], self.f0[:, 1])
        
        print("F0 Evaluation Metrics:", f0_evaluation)
        self.plot_f0()
                
        # reference_midi_path = Path(self.reference_midi_path)
        # output_midi_file = Path(self.output_midi_file)
        # precision, recall, f_measure, overlap_evaluation, ref_notes, out_notes = compare_midi_files(
        #                                                                             self,
        #                                                                             reference_midi_path, 
        #                                                                             output_midi_file
        #                                                                         )

        # print(f"Precision: {precision}")
        # print(f"Recall: {recall}")
        # print(f"F-measure: {f_measure}")
        # print(f"Overlap Evaluation: {overlap_evaluation}")
        
        # self.plot_MIDI(ref_notes, out_notes)
        # self.plot_summary(overlap_evaluation)
        
        
        
        
        # Plot f0
    def plot_f0(self):
        #time_stamps = np.arange(f0.shape[0]) * 256 / float(self.fs)

        plt.figure(figsize=(12, 6))
        plt.plot(self.f0[:, 0], self.f0[:, 1], label='Detected F0', color='blue')
        plt.plot(self.reference_f0[:, 0], self.reference_f0[:, 1], label='Reference F0', color='red')
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.title('Detected vs Reference F0')
        plt.legend()
        plt.show()
        #plt.savefig('tests/outputs/f0_comparison.png')
        # plt.close()
        
        # Plot MIDI Notes
    def plot_MIDI(self, ref_notes, det_notes):
        plt.figure(figsize=(12, 6))
        for i, (start, end, pitch) in enumerate(ref_notes):
            plt.plot([start, end], [pitch, pitch], color='red', label='Reference MIDI' if i == 0 else "")
        for i, (start, end, pitch) in enumerate(det_notes):
            plt.plot([start, end], [pitch, pitch], color='blue', label='Detected MIDI' if i == 0 else "")
        plt.xlabel('Time (s)')
        plt.ylabel('MIDI Pitch')
        plt.title('Detected vs Reference MIDI Notes')
        plt.legend()
        plt.show()
        # plt.savefig('tests/outputs/midi_comparison.png')
        # plt.close()


    def plot_summary(self, overlap_evaluation):
        plt.figure(figsize=(12, 6))
        metrics = ['Precision', 'Recall', 'F-measure']
        values = [overlap_evaluation['Precision'], overlap_evaluation['Recall'], overlap_evaluation['F-measure']]
        plt.bar(metrics, values, color=['blue', 'green', 'orange'])
        plt.ylim(0, 1)
        plt.xlabel('Metrics')
        plt.ylabel('Values')
        plt.title('Overall MIDI Transcription Metrics')
        plt.show()
        # plt.savefig('tests/outputs/summary_metrics.png')
        # plt.close()


    def test_invalid_audio_path(self):
        invalid_path = TESTS_DIR / 'Datasets/non_existent_file.wav'
        with self.assertRaises(FileNotFoundError):
            li.load(invalid_path)

    def test_invalid_f0_dir(self):
        invalid_f0_path = SRC_DIR / 'outputs/non_existent_file.csv'
        with self.assertRaises(FileNotFoundError):
            np.loadtxt(invalid_f0_path, delimiter=',')


    def test_f0_values(self):
        # Example test to verify f0 values
        self.assertTrue(np.all(self.f0[:, 1] >= 0.0), "F0 values should be non-negative frequencies")


    # def test_invalid_reference_f0(self):
    #     self.reference_f0 = np.loadtxt('tests/Datasets/non_existent_file.csv', delimiter=',')
    #     with self.assertRaises(FileNotFoundError):
    #         f0_evaluation = mir_eval.melody.evaluate(self.reference_f0[:, 0], self.reference_f0[:, 1], self.f0[:, 0], self.f0[:, 1])

    # def test_invalid_reference_midi(self):
    #     self.reference_midi = pretty_midi.PrettyMIDI('tests/Datasets/non_existent_file.mid')
    #     with self.assertRaises(FileNotFoundError):
    #         ref_notes = [(note.start, note.end, note.pitch) for inst in self.reference_midi.instruments for note in inst.notes]

    
# This script should read some MIDI file and to extract pitch and note annotations
# with an specific hopsize.

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
            print("Calculating time:", cumulated_time)
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
    print("note_list:", note_list)
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
        print("note.end:", note.end)
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


def midi2pitch(midi_path: Path) -> None:
    # (1) read midi file with mido
    # (2) extract note toggle messages.
    # (3) generate pitch annotations using an specific hopsize: <start-time> <Hz>
    # (4) generate note annotations: <onset> <offset> <midi-number>

    # initialize some parameters    
    #TODO: get hop_size and tempo from the audio2pitch() function
    sample_rate = 44100
    hop_size = 256  
    # read MIDI file
    mid = read_midi(midi_path)
    # extract a sequence of Notes
    tempo = 112.34714674 
    notes_list = get_notes_from_midi(mid, tempo)
    # generate pitch and notes annotations from MIDI file (groundtruth)
    pitch_gt, curve = notes_to_pitch_gt(sample_rate, hop_size, notes_list)
    notes_gt = notes_to_note_gt(notes_list)

    return pitch_gt, curve, notes_gt

def compare_midi_files(self, reference_midi_path: Path, output_midi_file: Path):
    # Read MIDI files
    ref_midi = read_midi(reference_midi_path)
    out_midi = read_midi(output_midi_file)
    
    # Extract notes from MIDI files
    tempo = 80  # Adjust this according to your needs or extract it from the MIDI file
    ref_notes = get_notes_from_midi(ref_midi, tempo)
    out_notes = get_notes_from_midi(out_midi, tempo)
    
    
    # Generate pitch and note annotations from MIDI files
    sample_rate = 44100
    hop_size = 64
    ref_pitch_gt, ref_curve = notes_to_pitch_gt(sample_rate, hop_size, ref_notes)
    out_pitch_gt, ref_curve = notes_to_pitch_gt(sample_rate, hop_size, out_notes)
    print("ref_pitch_gt shape:", ref_pitch_gt.shape)
    print("out_pitch_gt shape:", out_pitch_gt.shape)
    
    ref_notes_gt = notes_to_note_gt(ref_notes)
    out_notes_gt = notes_to_note_gt(out_notes)
    
    # Extract intervals and pitches for mir_eval
    ref_intervals = np.array([(note[0], note[1]) for note in ref_notes_gt])
    ref_notes = np.array([note[2] for note in ref_notes_gt])

    out_intervals = np.array([(note[0], note[1]) for note in out_notes_gt])
    out_notes = np.array([note[2] for note in out_notes_gt])

    # For numpy arrays
    print("Size of ref_intervals:", ref_intervals.shape)
    print("Size of ref_intervals:", ref_intervals.shape)
    print("Size of out_intervals:", out_intervals.shape)
    print("Size of ref_pitches:", self.reference_f0.shape)
    print("Size of est_pitches:", self.f0.shape)

    # For lists
    print("Size of ref_intervals:", len(ref_intervals))
    print("Size of out_intervals:", len(out_intervals))
    print("Size of ref_pitches:", len(self.reference_f0[:, 1]))
    print("Size of est_pitches:", len(self.f0[:, 1]))

    
    pitch_metrics = assess_notes(ref_intervals, self.reference_f0[:, 1], out_intervals, self.f0[:, 1])
    print("Pitch Metrics:", pitch_metrics)
    
    # Evaluate using mir_eval
    precision, recall, f_measure, _ = mir_eval.transcription.precision_recall_f1_overlap(
        ref_intervals, mir_eval.util.midi_to_hz(ref_curve),
        out_intervals, mir_eval.util.midi_to_hz(self.f0[:, 1]),
        onset_tolerance=0.05, offset_ratio=None, pitch_tolerance=50.0, beta=1.0
    )
    
    overlap_evaluation = mir_eval.transcription.evaluate(
        ref_intervals, mir_eval.util.midi_to_hz(self.reference_f0[:, 1]),
        out_intervals, mir_eval.util.midi_to_hz(self.f0[:, 1]),
        onset_tolerance=0.05, offset_ratio=None, pitch_tolerance=50.0
    )
    
    return precision, recall, f_measure, overlap_evaluation, ref_notes, out_notes

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


## METRICS
def assess_pitch(ref_time: list, ref_freq: list, est_time: list, est_freq: list):
    ref_voicing, ref_cent, est_voicing, est_cent = mir_eval.melody.to_cent_voicing(
        ref_time, ref_freq, est_time, est_freq
    )
    # TODO: consider activation segments - if segments are included in json file just assess voiced intervals
    # build some bins
    voicing, accuracy = (dict() for n in range(2))
    # estimate pitch metrics
    voicing["recall"], voicing["false_alarm"] = mir_eval.melody.voicing_measures(
        ref_voicing, est_voicing
    )
    accuracy["raw"] = mir_eval.melody.raw_pitch_accuracy(
        ref_voicing, ref_cent, est_voicing, est_cent
    )
    # provide a single dict
    return {"voicing": voicing, "accuracy": accuracy}


def assess_notes(
    ref_intervals: np.ndarray,
    ref_pitches: np.ndarray,
    est_intervals: np.ndarray,
    est_pitches: np.ndarray,
    onset_tolerance: float = 0.25,
    offset_ratio: float = 0.5,
):
    # validate annotations: intervals is Nx2 ndarray whereas pitches refers to Nx1 ndarray
    mir_eval.transcription.validate(
        ref_intervals, ref_pitches, est_intervals, est_pitches
    )
    # build some bins
    overlap, onset, offset = (dict() for n in range(3))

    # estimate note metrics
    (
        overlap["precision"],
        overlap["recall"],
        overlap["f_measure"],
        overlap["avg_overlap_ratio"],
    ) = mir_eval.transcription.precision_recall_f1_overlap(
        ref_intervals,
        ref_pitches,
        est_intervals,
        est_pitches,
        onset_tolerance=onset_tolerance,
        offset_ratio=offset_ratio,
    )

    (
        onset["precision"],
        onset["recall"],
        onset["f_measure"],
    ) = mir_eval.transcription.onset_precision_recall_f1(
        ref_intervals, est_intervals, onset_tolerance=onset_tolerance
    )

    (
        offset["precision"],
        offset["recall"],
        offset["f_measure"],
    ) = mir_eval.transcription.offset_precision_recall_f1(
        ref_intervals, est_intervals, offset_ratio=offset_ratio
    )

    # provide a single dict
    return {"overlap": overlap, "onset": onset, "offset": offset}

    
if __name__ == '__main__':
    unittest.main()
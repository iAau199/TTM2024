import numpy as np
import mir_eval
from pathlib import Path
from midi2pitch import read_midi, get_notes_from_midi, notes_to_note_gt


def compare_midi_files(self, reference_midi_path: Path, output_midi_file: Path):
    # Read MIDI files
    ref_midi = read_midi(reference_midi_path)
    out_midi = read_midi(output_midi_file)
    
    # Extract notes from MIDI files
    tempo = 112.34714674 
    ref_notes = get_notes_from_midi(ref_midi, tempo)
    out_notes = get_notes_from_midi(out_midi, tempo)
    
    ref_notes_gt = notes_to_note_gt(ref_notes)
    out_notes_gt = notes_to_note_gt(out_notes)
    
    # Extract intervals and pitches for mir_eval
    ref_intervals = np.array([(note[0], note[1]) for note in ref_notes_gt])
    ref_notes = np.array([note[2] for note in ref_notes_gt])

    out_intervals = np.array([(note[0], note[1]) for note in out_notes_gt])
    out_notes = np.array([note[2] for note in out_notes_gt])
    
    note_metrics = assess_notes(ref_intervals, mir_eval.util.midi_to_hz(ref_notes), out_intervals, mir_eval.util.midi_to_hz(out_notes))
    print("Pitch Metrics:", note_metrics)
    
    return note_metrics, ref_notes_gt, out_notes_gt


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
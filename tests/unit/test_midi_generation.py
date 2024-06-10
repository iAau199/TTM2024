import unittest
import numpy as np
import mir_eval
from src.pitch2midi import convert_to_midi
import pretty_midi

class TestMIDIGeneration(unittest.TestCase):
    def setUp(self):
        self.f0_csv = 'tests/output/f0.csv'
        self.output_midi_file = 'tests/output/output.mid'
        self.reference_midi = pretty_midi.PrettyMIDI('tests/data/reference_midi.mid')
    
    def test_note_overlap(self):
        convert_to_midi(self.f0_csv, self.output_midi_file)
        midi_data = pretty_midi.PrettyMIDI(self.output_midi_file)
        ref_notes = [(note.start, note.end, note.pitch) for inst in self.reference_midi.instruments for note in inst.notes]
        det_notes = [(note.start, note.end, note.pitch) for inst in midi_data.instruments for note in inst.notes]
        overlap_evaluation = mir_eval.transcription.precision_recall_f1_overlap(ref_notes, det_notes)
        self.assertGreaterEqual(overlap_evaluation['Precision'], 0.9, "Note overlap precision is below 90%")
        self.assertGreaterEqual(overlap_evaluation['Recall'], 0.9, "Note overlap recall is below 90%")
        self.assertGreaterEqual(overlap_evaluation['F-measure'], 0.9, "Note overlap F-measure is below 90%")

if __name__ == '__main__':
    unittest.main()

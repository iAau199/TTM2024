import os
import sys
import unittest
import numpy as np
import mir_eval
import librosa as li
from pathlib import Path
import evaluation as eval
import visualizations as vis
import midi2pitch as m2p

# Get the current working directory
script_dir = Path().resolve()
# Add the src directory to the sys.path
SRC_DIR = script_dir / "src"
TESTS_DIR = script_dir / "tests"
print(SRC_DIR)
print(TESTS_DIR)
sys.path.append(str(SRC_DIR))
sys.path.append(str(TESTS_DIR))

import Block_1_Audio2Pitch.audio2pitch as a2p
import Block_2_Pitch2MIDI.pitch2midi as p2m


class TestEndToEnd(unittest.TestCase):
    def setUp(self):
        self.audio_name = 'KSHMR-Guitar-100BPM-09'       
        self.audio_path = TESTS_DIR / 'Datasets/KSHMR-Guitar-100BPM-09.wav'
        self.f0_dir = SRC_DIR / 'outputs/f0_KSHMR-Guitar-100BPM-09.csv'
        self.output_midi_file = SRC_DIR / 'outputs/KSHMR-Guitar-100BPM-09_output.mid'
        self.reference_midi_path = TESTS_DIR / 'Datasets/KSHMR-Guitar-100BPM-09-MIDI.mid'
        
        self.assertTrue(os.path.exists(self.audio_path), "Test audio file does not exist")
        self.assertTrue(os.path.exists(self.f0_dir), "F0 CSV file does not exist")
        self.assertTrue(os.path.exists(self.output_midi_file), "Output MIDI file does not exist")
        self.assertTrue(os.path.exists(self.reference_midi_path), "Reference MIDI file does not exist")

        self.x, self.fs = li.load(self.audio_path)
        self.f0 = np.loadtxt(self.f0_dir, delimiter=',')
       

    def test_end_to_end(self):
        
        self.H, self.tempo, selected, time_f0 = a2p.audio2Pitch(self.audio_name)
        
        self.sampling_rate = 44100
        p2m.pitch2midi(self.H, self.tempo, self.sampling_rate, time_f0, self.audio_name)
        f0_evaluation = eval.pitch_evaluation(self)
        #print("\nF0 Evaluation Metrics:", f0_evaluation)
        vis.display_f0_evaluation_metrics(f0_evaluation)
        vis.plot_f0(self)
        
        # pitch_metrics = eval.assess_pitch(self.ref_f0_curve[:, 0], self.ref_f0_curve[:, 1], self.f0[:, 0], self.f0[:, 1])
        # print("\nPitch Metrics:", pitch_metrics)
        
        reference_midi_path = Path(self.reference_midi_path)
        output_midi_file = Path(self.output_midi_file)
        note_metrics, ref_notes, out_notes = eval.compare_midi_files(   
                                                                    self,
                                                                    reference_midi_path, 
                                                                    output_midi_file
                                                                )

        vis.plot_MIDI(ref_notes, out_notes)
        
        #print("\nNote Metrics:", note_metrics)
        vis.display_assess_notes_metrics(note_metrics)      
        

    def test_invalid_audio_path(self):
        invalid_path = TESTS_DIR / 'Datasets/non_existent_file.wav'
        with self.assertRaises(FileNotFoundError):
            li.load(invalid_path)

    def test_invalid_f0_dir(self):
        invalid_f0_path = SRC_DIR / 'outputs/non_existent_file.csv'
        with self.assertRaises(FileNotFoundError):
            np.loadtxt(invalid_f0_path, delimiter=',')

    def test_f0_values(self):
        self.assertTrue(np.all(self.f0[:, 1] >= 0.0), "F0 values should be non-negative frequencies")


if __name__ == '__main__':
    unittest.main()
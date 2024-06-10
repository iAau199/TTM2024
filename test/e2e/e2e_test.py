import os
import unittest
import numpy as np
import mir_eval
import librosa as li
import pretty_midi
import matplotlib.pyplot as plt
import src.Block_1_Audio2Pitch.audio2pitch as a2p
import src.Block_2_Pitch2MIDI.pitch2midi as p2m


class TestEndToEnd(unittest.TestCase):
    def setUp(self):
        self.audio_path = 'tests/Datasets/test_audio.wav'
        self.f0_dir = 'src/outputs/f0.csv'
        self.output_midi_file = 'src/outputs/output.mid'
        self.reference_f0_path = 'tests/Datasets/reference_f0.csv'
        self.reference_midi_path = 'tests/Datasets/reference_midi.mid'

        self.assertTrue(os.path.exists(self.audio_path), "Test audio file does not exist")
        self.assertTrue(os.path.exists(self.f0_dir), "F0 CSV file does not exist")
        self.assertTrue(os.path.exists(self.output_midi_file), "Output MIDI file does not exist")
        self.assertTrue(os.path.exists(self.reference_f0_path), "Reference f0 CSV file does not exist")
        self.assertTrue(os.path.exists(self.reference_midi_path), "Reference MIDI file does not exist")

        self.x, self.fs = li.load(self.audio_path)
        self.f0 = np.loadtxt(self.f0_dir, delimiter=',')
        self.reference_f0 = np.loadtxt(self.reference_f0_path, delimiter=',')
        self.reference_midi = pretty_midi.PrettyMIDI(self.reference_midi_path)
        self.midi_data = pretty_midi.PrettyMIDI(self.output_midi_file)
        

    def test_end_to_end(self):
        # Step 1: Pitch Detection
        # Load the f0 values from a CSV file

        # Step 2: Convert to MIDI
        self.assertIsNotNone(self.midi_data, "MIDI conversion failed")

        # Evaluation
        f0_evaluation = mir_eval.melody.evaluate(self.reference_f0[:, 0], self.reference_f0[:, 1], self.f0[:, 0], self.f0[:, 1])
        
        ref_notes = [(note.start, note.end, note.pitch) for inst in self.reference_midi.instruments for note in inst.notes]
        det_notes = [(note.start, note.end, note.pitch) for inst in self.midi_data.instruments for note in inst.notes]
        overlap_evaluation = mir_eval.transcription.precision_recall_f1_overlap(ref_notes, det_notes)
        
        # Statistics
        print("F0 Evaluation Metrics:", f0_evaluation)
        print("Overlap Evaluation Metrics:", overlap_evaluation)
        
        # Plotting
        #self.plot_results(f0, f0_evaluation, ref_notes, det_notes, overlap_evaluation)
        self.plot_f0(self)
        self.plot_MIDI(self, ref_notes, det_notes)
        self.plot_summary(self, overlap_evaluation)
        
        # Assertions
        self.assertGreaterEqual(f0_evaluation['Overall Accuracy'], 0.9, "Pitch accuracy is below 90%")
        
        self.assertGreaterEqual(overlap_evaluation['Precision'], 0.9, "Note overlap precision is below 90%")
        self.assertGreaterEqual(overlap_evaluation['Recall'], 0.9, "Note overlap recall is below 90%")
        self.assertGreaterEqual(overlap_evaluation['F-measure'], 0.9, "Note overlap F-measure is below 90%")

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
        plt.savefig('tests/output/f0_comparison.png')
        
        # Plot MIDI Notes
    def plot_MIDI(self, ref_notes, det_notes):
        plt.figure(figsize=(12, 6))
        for start, end, pitch in ref_notes:
            plt.plot([start, end], [pitch, pitch], color='red', label='Reference MIDI' if start == ref_notes[0][0] else "")
        for start, end, pitch in det_notes:
            plt.plot([start, end], [pitch, pitch], color='blue', label='Detected MIDI' if start == det_notes[0][0] else "")
        plt.xlabel('Time (s)')
        plt.ylabel('MIDI Pitch')
        plt.title('Detected vs Reference MIDI Notes')
        plt.legend()
        plt.savefig('tests/output/midi_comparison.png')

    def plot_summary(self, overlap_evaluation):
        # Summary Plot
        plt.figure(figsize=(12, 6))
        metrics = ['Precision', 'Recall', 'F-measure']
        values = [overlap_evaluation['Precision'], overlap_evaluation['Recall'], overlap_evaluation['F-measure']]
        plt.bar(metrics, values, color=['blue', 'green', 'orange'])
        plt.ylim(0, 1)
        plt.xlabel('Metrics')
        plt.ylabel('Values')
        plt.title('Overall MIDI Transcription Metrics')
        plt.savefig('tests/output/summary_metrics.png')

    # checking paths
    def test_invalid_audio_path(self):
        self.audio_path = 'tests/Datasets/non_existent_file.wav'
        with self.assertRaises(FileNotFoundError):
            self.x, self.fs = li.load(self.audio_path)

    def test_invalid_f0_dir(self):
        self.f0_dir = 'src/outputs/non_existent_file.csv'
        with self.assertRaises(FileNotFoundError):
            self.f0 = np.loadtxt(self.f0_dir, delimiter=',')

    def test_invalid_output_midi_file(self):
        self.output_midi_file = 'src/outputs/non_existent_file.mid'
        with self.assertRaises(FileNotFoundError):
            self.midi_data = pretty_midi.PrettyMIDI(self.output_midi_file)

    def test_invalid_reference_f0(self):
        self.reference_f0 = np.loadtxt('tests/Datasets/non_existent_file.csv', delimiter=',')
        with self.assertRaises(FileNotFoundError):
            f0_evaluation = mir_eval.melody.evaluate(self.reference_f0[:, 0], self.reference_f0[:, 1], self.f0[:, 0], self.f0[:, 1])

    def test_invalid_reference_midi(self):
        self.reference_midi = pretty_midi.PrettyMIDI('tests/Datasets/non_existent_file.mid')
        with self.assertRaises(FileNotFoundError):
            ref_notes = [(note.start, note.end, note.pitch) for inst in self.reference_midi.instruments for note in inst.notes]

    
if __name__ == '__main__':
    unittest.main()

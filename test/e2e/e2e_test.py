import unittest
import numpy as np
import mir_eval
import librosa as li
import pretty_midi
import matplotlib.pyplot as plt
from src.audio2pitch import f0Detection
from src.pitch2midi import convert_to_midi

class TestEndToEnd(unittest.TestCase):
    def setUp(self):
        self.audio_path = 'sounds/test_audio.wav'
        self.x, self.fs = li.load(self.audio_path)
        self.output_midi_file = 'tests/output/output.mid'
        self.reference_f0 = np.loadtxt('tests/data/reference_f0.csv', delimiter=',')
        self.reference_midi = pretty_midi.PrettyMIDI('tests/data/reference_midi.mid')

    def test_end_to_end(self):
        # Step 1: Pitch Detection
        window = 'hamming'
        M = 8000
        N = 8192
        H = 256
        t = -55
        minf0 = 120
        maxf0 = 500
        w = li.filters.get_window(window, M)
        f0 = f0Detection(self.x, self.fs, w, N, H, t, minf0, maxf0, 10)
        np.savetxt('tests/output/f0.csv', f0, delimiter=',', fmt='%s')

        # Step 2: Convert to MIDI
        convert_to_midi('tests/output/f0.csv', self.output_midi_file)
        midi_data = pretty_midi.PrettyMIDI(self.output_midi_file)
        self.assertIsNotNone(midi_data, "MIDI conversion failed")

        # Evaluation
        f0_evaluation = mir_eval.melody.evaluate(self.reference_f0[:, 0], self.reference_f0[:, 1], f0[:, 0], f0[:, 1])
        ref_notes = [(note.start, note.end, note.pitch) for inst in self.reference_midi.instruments for note in inst.notes]
        det_notes = [(note.start, note.end, note.pitch) for inst in midi_data.instruments for note in inst.notes]
        overlap_evaluation = mir_eval.transcription.precision_recall_f1_overlap(ref_notes, det_notes)
        
        # Statistics
        print("F0 Evaluation Metrics:", f0_evaluation)
        print("Overlap Evaluation Metrics:", overlap_evaluation)
        
        # Plotting
        self.plot_results(f0, f0_evaluation, ref_notes, det_notes, overlap_evaluation)
        
        # Assertions
        self.assertGreaterEqual(f0_evaluation['Overall Accuracy'], 0.9, "Pitch accuracy is below 90%")
        self.assertGreaterEqual(overlap_evaluation['Precision'], 0.9, "Note overlap precision is below 90%")
        self.assertGreaterEqual(overlap_evaluation['Recall'], 0.9, "Note overlap recall is below 90%")
        self.assertGreaterEqual(overlap_evaluation['F-measure'], 0.9, "Note overlap F-measure is below 90%")

    def plot_results(self, f0, f0_evaluation, ref_notes, det_notes, overlap_evaluation):
        time_stamps = np.arange(f0.shape[0]) * 256 / float(self.fs)

        # Plot F0
        plt.figure(figsize=(12, 6))
        plt.plot(time_stamps, f0[:, 1], label='Detected F0', color='blue')
        plt.plot(self.reference_f0[:, 0], self.reference_f0[:, 1], label='Reference F0', color='red')
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.title('Detected vs Reference F0')
        plt.legend()
        plt.savefig('tests/output/f0_comparison.png')

        # Plot MIDI Notes
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

if __name__ == '__main__':
    unittest.main()

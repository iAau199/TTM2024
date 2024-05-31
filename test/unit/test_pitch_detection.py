import unittest
import numpy as np
import mir_eval
import librosa as li
from src.audio2pitch import detect_onsets, detect_offsets, HM

class TestPitchDetection(unittest.TestCase):

    def setUp(self):
        self.audio_file = 'Datasets/test_audio.wav'
        self.x, self.fs = li.load(self.audio_file)
        self.reference_f0 = np.loadtxt('tests/reference_data/reference_f0.csv')
        self.reference_onsets = np.loadtxt('tests/reference_data/reference_onsets.txt')
        self.reference_offsets = np.loadtxt('tests/reference_data/reference_offsets.txt')

    def test_pitch_accuracy(self):
        window = 'hamming'
        M = 8000
        N = 8192
        H = 256
        f0et = 10
        t = -55
        minf0 = 120
        maxf0 = 500
        w = li.filters.get_window(window, M)
        f0 = HM.f0Detection(self.x, self.fs, w, N, H, t, minf0, maxf0, f0et)
        f0_evaluation = mir_eval.melody.evaluate(self.reference_f0[:, 0], self.reference_f0[:, 1], f0[:, 0], f0[:, 1])
        self.assertGreaterEqual(f0_evaluation['Overall Accuracy'], 0.9, "Pitch accuracy is below 90%")

    def test_onset_detection(self):
        onsets = detect_onsets(self.x, self.fs)
        onset_evaluation = mir_eval.onset.evaluate(self.reference_onsets, onsets)
        self.assertGreaterEqual(onset_evaluation['Precision'], 0.9, "Onset precision is below 90%")

    def test_offset_detection(self):
        offsets = detect_offsets(self.x, self.fs)
        offset_evaluation = mir_eval.onset.evaluate(self.reference_offsets, offsets)
        self.assertGreaterEqual(offset_evaluation['Precision'], 0.9, "Offset precision is below 90%")

if __name__ == '__main__':
    unittest.main()

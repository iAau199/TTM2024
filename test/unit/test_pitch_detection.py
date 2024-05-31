import unittest
import numpy as np
import mir_eval
from src.audio2pitch import f0Detection
import librosa as li

class TestPitchDetection(unittest.TestCase):
    def setUp(self):
        self.audio_path = 'sounds/test_audio.wav'
        self.x, self.fs = li.load(self.audio_path)
        self.reference_f0 = np.loadtxt('tests/data/reference_f0.csv', delimiter=',')

    def test_pitch_accuracy(self):
        window = 'hamming'
        M = 8000
        N = 8192
        H = 256
        t = -55
        minf0 = 120
        maxf0 = 500
        w = li.filters.get_window(window, M)
        f0 = f0Detection(self.x, self.fs, w, N, H, t, minf0, maxf0, 10)
        f0_evaluation = mir_eval.melody.evaluate(self.reference_f0[:, 0], self.reference_f0[:, 1], f0[:, 0], f0[:, 1])
        self.assertGreaterEqual(f0_evaluation['Overall Accuracy'], 0.9, "Pitch accuracy is below 90%")

    def test_voiced_measures(self):
        window = 'hamming'
        M = 8000
        N = 8192
        H = 256
        t = -55
        minf0 = 120
        maxf0 = 500
        w = li.filters.get_window(window, M)
        f0 = f0Detection(self.x, self.fs, w, N, H, t, minf0, maxf0, 10)
        voiced_measures = mir_eval.melody.voicing_measures(self.reference_f0[:, 1], f0[:, 1])
        self.assertGreaterEqual(voiced_measures['Voicing Recall'], 0.9, "Voicing recall is below 90%")
        self.assertGreaterEqual(voiced_measures['Voicing False Alarm'], 0.1, "Voicing false alarm is above 10%")

    def test_onset_detection(self):
        onsets = mir_eval.onset.detect_onsets(self.x, self.fs)
        onset_evaluation = mir_eval.onset.evaluate(self.reference_f0[:, 0], onsets)
        self.assertGreaterEqual(onset_evaluation['Precision'], 0.9, "Onset precision is below 90%")
        self.assertGreaterEqual(onset_evaluation['Recall'], 0.9, "Onset recall is below 90%")
        self.assertGreaterEqual(onset_evaluation['F-measure'], 0.9, "Onset F-measure is below 90%")

    def test_offset_detection(self):
        offsets = mir_eval.onset.detect_offsets(self.x, self.fs)
        offset_evaluation = mir_eval.onset.evaluate(self.reference_f0[:, 0], offsets)
        self.assertGreaterEqual(offset_evaluation['Precision'], 0.9, "Offset precision is below 90%")
        self.assertGreaterEqual(offset_evaluation['Recall'], 0.9, "Offset recall is below 90%")
        self.assertGreaterEqual(offset_evaluation['F-measure'], 0.9, "Offset F-measure is below 90%")

if __name__ == '__main__':
    unittest.main()

import unittest
import numpy as np
import mir_eval
import pretty_midi
from src.audio2pitch import detect_onsets, detect_offsets, HM
from src.pitch2midi import convert_to_midi
import librosa as li

class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.audio_file = 'sounds/test_audio.wav'
        self.x, self.fs = li.load(self.audio_file)
        self.reference_f0 = np.loadtxt('tests/reference_data/reference_f0.csv')
        self.reference_onsets = np.loadtxt('tests/reference_data/reference_onsets.txt')
        self.reference_offsets = np.loadtxt('tests/reference_data/reference_offsets.txt')
        self.output_midi_file = 'tests/output/output.midi'

    def test_integration_audio_to_midi(self):
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
        np.savetxt('tests/output/f0.csv', f0, delimiter=',', fmt='%s')
        convert_to_midi('tests/output/f0.csv', self.output_midi_file)
        midi_data = pretty_midi.PrettyMIDI(self.output_midi_file)
        self.assertIsNotNone(midi_data, "MIDI conversion failed")

if __name__ == '__main__':
    unittest.main()

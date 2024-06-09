import unittest
import time
import numpy as np
import librosa as li
from src.audio2pitch import f0Detection
from src.pitch2midi import convert_to_midi

class TestPerformance(unittest.TestCase):
    def setUp(self):
        self.audio_path = 'sounds/test_audio.wav'
        self.x, self.fs = li.load(self.audio_path)

    def test_performance(self):
        start_time = time.time()
        
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
        detection_time = time.time()
        
        # Step 2: Convert to MIDI
        np.savetxt('tests/output/f0.csv', f0, delimiter=',', fmt='%s')
        convert_to_midi('tests/output/f0.csv', 'tests/output/output.mid')
        conversion_time = time.time()

        detection_duration = detection_time - start_time
        conversion_duration = conversion_time - detection_time

        print(f"Pitch detection duration: {detection_duration:.2f} seconds")
        print(f"MIDI conversion duration: {conversion_duration:.2f} seconds")

        self.assertLessEqual(detection_duration, 5.0, "Pitch detection took too long")
        self.assertLessEqual(conversion_duration, 2.0, "MIDI conversion took too long")

if __name__ == '__main__':
    unittest.main()

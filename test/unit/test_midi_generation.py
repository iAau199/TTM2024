import unittest
import pretty_midi
from src.pitch2midi import convert_to_midi

class TestMIDIGeneration(unittest.TestCase):

    def setUp(self):
        self.f0_file = 'tests/output/f0.csv'
        self.output_midi_file = 'tests/output/output.midi'

    def test_midi_conversion(self):
        convert_to_midi(self.f0_file, self.output_midi_file)
        midi_data = pretty_midi.PrettyMIDI(self.output_midi_file)
        self.assertIsNotNone(midi_data, "MIDI conversion failed")

if __name__ == '__main__':
    unittest.main()

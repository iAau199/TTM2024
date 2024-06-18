# TuneTrek

Audio2Midi Converter TuneTrek is a tool created to convert audio signals into MIDI (Musical Instrument Digital Interface) data.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

Follow these steps to set up the project in a Python virtual environment:

1. **Clone the repository:**

    ```sh
    https://github.com/iAau199/TTM2024.git
    cd TTM2024
    ```

2. **Create and activate a virtual environment:**

    On Windows:
    
    ```sh
    python -m venv venv
    venv\Scripts\activate
    ```

    On macOS and Linux:
    
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

Now you're ready to use TuneTrek!

# Audio to MIDI Converter App

This Python application allows users to convert audio files into MIDI format using a simple graphical interface. Below are the instructions on how to use the app effectively:


## Usage

1. **Launch the Application**

   Run the application by executing the `audio2MIDI_App.py` script. This will open a graphical interface where you can interact with the app.

   ```bash
   python audio2MIDI_App.py
   ```

2. **Select an Audio File**

   Click on the "Select File" button to choose an audio file (supported format: `.wav`). Once selected, the filename will be displayed.

3. **Choose Audio Type**

   - **Melodies (120-500 Hz)**: Select this option if your audio contains melodies with fundamental frequencies between 120 Hz and 500 Hz.
   - **Human Voice**: Choose this option for audios containing human voice.
   - **Instrumental Audios**: Select this for instrumental audios (in progress).
   - **Custom**: Allows you to specify custom frequency ranges. Enter the minimum and maximum frequencies in the provided fields.

4. **Adjust Frequency Range (Custom Option Only)**

   If you choose the "Custom" option and wish to adjust the frequency range after plotting the spectrogram, click "Yes" when prompted. Enter new minimum and maximum pitch ranges in the pop-up dialog.

5. **Plot Spectrogram**

   Enable the "Plot Spectrogram" checkbox if you want to visualize the spectrogram of the audio file before conversion.

6. **Convert**

   Click the "Convert" button to start the conversion process. The app will perform audio-to-pitch analysis, plot the spectrogram if selected, and then convert the detected pitches into MIDI format.

7. **Adjust min/max freq.**

   After plotting the spectrogram a prompt will allow you to modify the minimum and maximum frequencies. Enter new values as needed.

8. **Conversion Results**

   After conversion, MIDI files will be saved in the `src/outputs` directory. The app will also display a success message upon completion.

## Directory Structure
```
audio2midi/
│
├── src/
│   ├── audio2pitch.py
│   └── pitch2midi.py
│
└── tests/
    ├── unit/
    │   ├── test_pitch_detection.py
    │   └── test_midi_generation.py
    │
    ├── integration/
    │   └── test_integration.py
    │
    ├── e2e/
    │   └── test_end_to_end.py
    │
    └── performance/
        └── test_performance.py
```


## License

This work is licensed under CC BY-SA 4.0 - see the [LICENSE.md](LICENSE.md) file for details.

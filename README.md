# TuneTrek

<p align="center">
  <img src="TuneTrek.png" alt="Logo" style="width: 300px;"/>
</p>

TuneTrek is an innovative tool designed to convert audio signals into MIDI (Musical Instrument Digital Interface) data, unlocking new possibilities for creativity and musical expression. By bridging the gap between audio and MIDI, TuneTrek empowers musicians and creators to manipulate and control musical elements such as note pitches, velocities, and durations, allowing seamless integration of acoustic and software-based instruments within a MIDI-based workflow. This project embodies our enthusiasm for combining technology and music, pushing the boundaries of audio signal processing.

## Table of Contents

- [Installation](#installation)
- [Audio to MIDI Converter App](#audio-to-midi-converter-app)
- [Directory Structure](#directory-structure)
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


## Audio to MIDI Converter App

This Python application allows users to convert audio files into MIDI format using a simple graphical interface. Below are the instructions on how to use the app effectively:

### Usage

1. **Launch the Application**

   Run the application by executing the `audio2MIDI_App.py` script. This will open a graphical interface where you can interact with the app.

   ```bash
   python src/audio2MIDI_App.py
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
│   ├── Block_1_Audio2Pitch/
│   │   ├── audio2midi.py
│   │   └── ... 
│   │   
│   ├── Block_2_Pitch2MIDI/
│   │   ├── pitch2midi.py
│   │   └── ... 
│   │   
│   ├── outputs/
│   │
│   ├── audio2MIDI_App.py
│   │   
│   └── audio2midi.py
│
└── tests/
    ├── Datasets/
    │   ├── piano.waw
    │   ├── piano-MIDI.mid
    │   └── ... 
    │  
    ├── outputs/ 
    │  
    ├── ... 
    │  
    ├── visualizations.py
    ├── midi2pitch.py
    ├── evaluation.py
    │ 
    └── e2e_test.py
```

## License

This work is licensed under CC BY-SA 4.0 - see the [LICENSE.md](LICENSE.md) file for details.

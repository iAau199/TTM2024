# TuneTrek

Audio2Midi Converter TuneTrek is a tool created to convert audio signals into MIDI (Musical Instrument Digital Interface) data.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
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


## Usage

To use TuneTrek for converting audio files to MIDI, follow these steps:

1. **Navigate to the root directory of the project.**

2. **Run the main script:**

    ```sh
    python src/audio2midi.py
    ```

3. **Input the audio file name:**

    When prompted, enter the name of the audio file you want to convert. This audio file should be located in the `tests/Datasets` directory.

4. **Select the audio type and frequency range:**

    You will be prompted to select the type of audio and the corresponding frequency range. Choose from the following options:

    - **[1]** Melodies with fundamental frequency between 120 and 500 Hz
    - **[2]** Human voice (choose low or high frequencies)
    - **[3]** Instrumental audios (choose low, medium, or high frequencies)
    - **[4]** Custom option (input your desired pitch range)

    After selecting an option, an image of the audio spectrogram will appear.

    **Note:** Whenever an image is displayed, you need to close the image window for the code to continue executing.

5. **Adjust the frequency range if needed:**

    You will be asked if you want to adjust the minimum and maximum frequencies. Answer with **y** (yes) or **n** (no). If you choose **y**, you will be prompted to enter the new frequency ranges.


## Audio to MIDI Converter App

This Python application allows users to convert audio files into MIDI format using a simple graphical interface. Below are the instructions on how to use the app effectively:

### Usage

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
# TuneTrek

Audio2Midi Converter TuneTrek is a tool created to convert audio signals into MIDI (Musical Instrument Digital Interface) data.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
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


## License

This work is licensed under CC BY-SA 4.0 - see the [LICENSE.md](LICENSE.md) file for details.

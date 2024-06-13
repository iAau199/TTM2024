import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import matplotlib.pyplot as plt
import numpy as np
import librosa as li
from PIL import Image, ImageTk
from scipy.signal import get_window, medfilt
from scipy.ndimage import gaussian_filter1d
from Block_1_Audio2Pitch import audio2pitch as a2p
from Block_2_Pitch2MIDI import pitch2midi as p2m

# Function to handle file selection
def select_file():
    global selected_file_path
    selected_file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav")])
    if selected_file_path:
        file_label.config(text=f"Selected File: {os.path.basename(selected_file_path)}")

# Function to convert the selected file
def convert_file():
    audio_type = audio_type_var.get()
    custom_min_freq = min_freq_entry.get()
    custom_max_freq = max_freq_entry.get()
    flag = flag_var.get()

    if not selected_file_path:
        messagebox.showerror("Error", "Please select a file.")
        return

    if audio_type == "Melodies (120-500 Hz)":
        audio_type_code = 1
        min_freq = 120
        max_freq = 500
    elif audio_type == "Human Voice":
        audio_type_code = 2
        min_freq = 500
        max_freq = 1000
    elif audio_type == "Instrumental Audios":
        audio_type_code = 3
        min_freq = 80
        max_freq = 10000
    elif audio_type == "Custom":
        audio_type_code = 4
        if not custom_min_freq or not custom_max_freq:
            messagebox.showerror("Error", "Please enter valid frequency ranges for Custom option.")
            return
        try:
            min_freq = int(custom_min_freq)
            max_freq = int(custom_max_freq)
        except ValueError:
            messagebox.showerror("Error", "Frequency ranges must be integers.")
            return

    try:
        audioName = audioName = os.path.splitext(os.path.basename(selected_file_path))[0]
        H, tempo, selected, time_f0 = a2p.audio2Pitch(audioName, flag, audio_type_code, min_freq, max_freq)
        sampling_rate = 44100
        
        p2m.pitch2midi(H, tempo, sampling_rate, time_f0, audioName)
        messagebox.showinfo("Success", "Conversion completed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Conversion failed: {e}")

# Initialize Tkinter app
app = tk.Tk()
app.title("Audio to MIDI Converter")

# Load logo and name images

# Load and display logo
logo_path = 'TuneTrek.png'
if os.path.exists(logo_path):
    logo_img = Image.open(logo_path)
    logo_img = logo_img.resize((100, 104)) 
    logo_img = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(app, image=logo_img)
    logo_label.pack(pady=10)


# File selection frame
file_frame = tk.Frame(app)
file_frame.pack(pady=10)

file_label = tk.Label(file_frame, text="Selected File: None")
file_label.pack()

select_button = tk.Button(file_frame, text="Select File", command=select_file)
select_button.pack(pady=10)

# Audio type selection frame
audio_type_var = tk.StringVar()
audio_type_frame = tk.LabelFrame(app, text="Select Audio Type")
audio_type_frame.pack(pady=20)

audio_types = ["Melodies (120-500 Hz)", "Human Voice", "Instrumental Audios", "Custom"]
for audio_type in audio_types:
    rb = tk.Radiobutton(audio_type_frame, text=audio_type, variable=audio_type_var, value=audio_type)
    rb.pack(anchor=tk.W)

# Custom frequency range entry frame
custom_frame = tk.LabelFrame(app, text="Custom Frequency Range")
custom_frame.pack(pady=20)

min_freq_label = tk.Label(custom_frame, text="Minimum Frequency:")
min_freq_label.grid(row=0, column=0, padx=10, pady=5)
min_freq_entry = tk.Entry(custom_frame)
min_freq_entry.grid(row=0, column=1, padx=10, pady=5)

max_freq_label = tk.Label(custom_frame, text="Maximum Frequency:")
max_freq_label.grid(row=1, column=0, padx=10, pady=5)
max_freq_entry = tk.Entry(custom_frame)
max_freq_entry.grid(row=1, column=1, padx=10, pady=5)

# Flag selection (for plotting spectrogram) frame
flag_var = tk.IntVar()
flag_frame = tk.LabelFrame(app, text="Flag for Plotting Spectrogram")
flag_frame.pack(pady=20)

flag_checkbox = tk.Checkbutton(flag_frame, text="Plot Spectrogram", variable=flag_var, onvalue=1, offvalue=0)
flag_checkbox.pack()

# Convert button
convert_button = tk.Button(app, text="Convert", command=convert_file)
convert_button.pack(pady=20)

# Run the Tkinter main loop
app.mainloop()

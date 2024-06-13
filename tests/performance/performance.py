import time
import sys
from pathlib import Path

script_dir = Path().resolve()
SRC_DIR = script_dir / "src"
sys.path.append(str(SRC_DIR))
from audio2midi import audio2midi

def measure_performance():
    start_time = time.time()
    
    audioName = 'piano'
    audio2midi(audioName, flag=0)

    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Execution time: {execution_time} seconds")

measure_performance()
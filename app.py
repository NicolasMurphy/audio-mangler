

# Randomly samples chunks from multiple .wav files and concatenates them
# first iteration - missing details such as limiting fize size, normalization, 
# expected length of the chunks, more to follow. 

import os
import random
import numpy as np
from scipy.io import wavfile
from typing import List, Tuple

def load_audio(filename: str) -> Tuple[int, np.ndarray]:
    """Load WAV file and convert to mono float32"""
    sample_rate, data = wavfile.read(filename)
    if data.ndim == 2:
        data = np.mean(data, axis=1)
    return sample_rate, data.astype(np.float32)


def save_audio(filename: str, sample_rate: int, data: np.ndarray):
    """Save audio array to WAV format with 16-bit clipping"""
    clipped = np.clip(data, -32768, 32767).astype(np.int16)
    wavfile.write(filename, sample_rate, clipped)


def select_random_segment(data: np.ndarray, segment_length: int) -> np.ndarray:
    """Select a random segment from audio of given length (samples)"""
    if len(data) <= segment_length:
        return data
    start = random.randint(0, len(data) - segment_length)
    return data[start:start + segment_length]


def gather_random_samples(
    file_paths: List[str], segment_length: int
) -> Tuple[int, np.ndarray]:
    """Extract and concatenate random segments from multiple files"""
    all_segments = []
    sample_rate = None

    for path in file_paths:
        rate, data = load_audio(path)
        if sample_rate is None:
            sample_rate = rate
        elif rate != sample_rate:
            raise ValueError(f"Sample rate mismatch: {rate} != {sample_rate}")
        segment = select_random_segment(data, segment_length)
        all_segments.append(segment)

    return sample_rate, np.concatenate(all_segments)


def process_folder(
    folder: str, output_path: str, segment_length: int = 22050
):
    """Sample from all WAVs in a folder and create a concatenated output"""
    wav_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".wav")]
    rate, result = gather_random_samples(wav_files, segment_length)
    save_audio(output_path, rate, result)


if __name__ == "__main__":
    process_folder("samples", "output.wav")


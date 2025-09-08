
import numpy as np
from scipy.io import wavfile
from typing import Tuple

GOLDEN_RATIO = (1 + np.sqrt(5)) / 2


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


def scramble_chunks(
    data: np.ndarray, chunk_size: int, ratio: float = GOLDEN_RATIO
) -> np.ndarray:
    """Reorder audio chunks using golden ratio quasi-random permutation"""
    num_chunks = len(data) // chunk_size
    chunks = np.array_split(data[: num_chunks * chunk_size], num_chunks)
    indices = np.arange(num_chunks)
    perm = np.argsort(np.cos(indices * np.pi * ratio))
    scrambled = np.concatenate([chunks[i] for i in perm])
    return np.append(scrambled, data[num_chunks * chunk_size:])


def process_file(input_path: str, output_path: str, chunk_size: int = 2000):
    """End-to-end scrambler for a WAV file"""
    rate, audio = load_audio(input_path)
    scrambled = scramble_chunks(audio, chunk_size)
    save_audio(output_path, rate, scrambled)


if __name__ == "__main__":
    process_file("homemade-break-3.wav", "output.wav")


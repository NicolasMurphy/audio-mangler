# audio_mangler.py
"""
Randomly samples chunks from multiple .wav files and concatenates them.
Now includes:
- CLI interface
- Sample rate resampling
- Normalization
- Max file size filter
- Logging
"""

import os
import random
import logging
import argparse
import numpy as np
from typing import List, Tuple
from scipy.io import wavfile
from scipy.signal import resample_poly


def load_audio(filename: str) -> Tuple[int, np.ndarray]:
    """Load WAV file and convert to mono float32"""
    try:
        sample_rate, data = wavfile.read(filename)
        if data.ndim == 2:
            data = np.mean(data, axis=1)
        return sample_rate, data.astype(np.float32)
    except Exception as e:
        logging.warning(f"Error reading {filename}: {e}")
        return -1, np.array([])


def normalize_audio(data: np.ndarray) -> np.ndarray:
    """Normalize audio data to [-1.0, 1.0]"""
    peak = np.max(np.abs(data))
    return data / peak if peak > 0 else data


def resample_audio(data: np.ndarray, orig_sr: int, target_sr: int) -> np.ndarray:
    """Resample audio using polyphase method"""
    if orig_sr == target_sr:
        return data
    gcd = np.gcd(orig_sr, target_sr)
    up = target_sr // gcd
    down = orig_sr // gcd
    return resample_poly(data, up, down)


def save_audio(filename: str, sample_rate: int, data: np.ndarray):
    """Save audio as int16 WAV"""
    clipped = np.clip(data * 32767, -32768, 32767).astype(np.int16)
    wavfile.write(filename, sample_rate, clipped)


def select_random_segment(data: np.ndarray, segment_length: int) -> np.ndarray:
    """Pick a random segment of fixed length"""
    if len(data) <= segment_length:
        return data
    start = random.randint(0, len(data) - segment_length)
    return data[start:start + segment_length]


def gather_random_samples(
    file_paths: List[str],
    segment_length: int,
    normalize: bool,
    target_rate: int,
    max_filesize_mb: float
) -> Tuple[int, np.ndarray]:
    """Process WAV files and concatenate sampled segments"""
    all_segments = []
    sample_rate = target_rate

    for path in file_paths:
        if max_filesize_mb:
            size_mb = os.path.getsize(path) / (1024 * 1024)
            if size_mb > max_filesize_mb:
                logging.info(f"Skipping {path} ({size_mb:.2f} MB)")
                continue

        rate, data = load_audio(path)
        if data.size == 0:
            continue

        if rate != target_rate:
            logging.info(f"Resampling {path} from {rate}Hz → {target_rate}Hz")
            data = resample_audio(data, rate, target_rate)

        if normalize:
            data = normalize_audio(data)

        segment = select_random_segment(data, segment_length)
        all_segments.append(segment)

    if not all_segments:
        raise RuntimeError("No valid segments found.")

    return sample_rate, np.concatenate(all_segments)


def process_folder(
    folder: str,
    output_path: str,
    segment_length: int,
    normalize: bool,
    target_rate: int,
    max_filesize_mb: float
):
    """Main logic to process folder and save output"""
    wav_files = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith(".wav")
    ]

    if not wav_files:
        raise FileNotFoundError(f"No .wav files in folder: {folder}")

    rate, result = gather_random_samples(
        wav_files,
        segment_length,
        normalize,
        target_rate,
        max_filesize_mb
    )

    save_audio(output_path, rate, result)
    logging.info(f"✅ Saved output to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Random WAV segment sampler")
    parser.add_argument("input_folder", help="Folder containing WAV files")
    parser.add_argument("output_file", help="Where to save the output WAV")
    parser.add_argument("--segment_length", type=int, default=48000, help="Segment length in samples")
    parser.add_argument("--target_rate", type=int, default=48000, help="Target sample rate (Hz)")
    parser.add_argument("--normalize", action="store_true", help="Normalize audio before sampling")
    parser.add_argument("--max_filesize_mb", type=float, help="Skip files larger than this size")
    parser.add_argument("--loglevel", default="INFO", help="Logging level (DEBUG, INFO, WARNING, ERROR)")

    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel.upper(), format="%(levelname)s: %(message)s")

    try:
        process_folder(
            args.input_folder,
            args.output_file,
            args.segment_length,
            args.normalize,
            args.target_rate,
            args.max_filesize_mb,
        )
    except Exception as e:
        logging.error(f"❌ Error: {e}")


if __name__ == "__main__":
    main()


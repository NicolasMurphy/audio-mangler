"""
Audio scrambler using golden ratio for chunk reordering.
Golden ratio creates quasi-random permutation patterns.
"""

import numpy as np
from scipy.io import wavfile

sample_rate, data = wavfile.read("homemade-break-3.wav")

if data.ndim == 2:
    mono_data = np.mean(data, axis=1).astype(np.float32)
else:
    mono_data = data.astype(np.float32)

# sample_rate = 44100
# mono_data = np.array([0,1000,2000,3000,4000,5000,6000,7000,8000,-1000,-2000,-3000,-4000])

chunk_size = 2000
num_chunks = len(mono_data) // chunk_size
chunks = np.array_split(mono_data[: num_chunks * chunk_size], num_chunks)

# print("before mangling: ", chunks)

indices = np.arange(num_chunks)
golden = (1 + np.sqrt(5)) / 2
perm = np.argsort(np.cos(indices * np.pi * golden))

mangled = np.concatenate([chunks[i] for i in perm])
mangled = np.append(mangled, mono_data[num_chunks * chunk_size :])
# print("after mangling: ", mangled)
mangled = np.clip(mangled, -32768, 32767).astype(np.int16)

wavfile.write("output.wav", sample_rate, mangled)

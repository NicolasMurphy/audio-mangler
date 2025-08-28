import numpy as np
from scipy.io import wavfile

rate, data = wavfile.read('homemade-break-3.wav')

# Reverse and amplify 10x (distort)
mangled = np.clip(data[::-1] * 10, -32768, 32767).astype(np.int16)

wavfile.write('output.wav', rate, mangled)

import matplotlib.pyplot as plt
import numpy as np
import struct
from scipy.signal import butter, filtfilt

from src.cryptographer.model.audio_model import AudioFileHandler

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y

def unpack_audio_data(data, n_frames, n_channels, sampwidth):
    if sampwidth == 3:
        fmt = '<i'
        def unpack_fn(bytes_):
            return struct.unpack(fmt, bytes_ + (b'\x00' if bytes_[2] < 0x80 else b'\xff'))[0]
    elif sampwidth == 2:
        fmt = '<h'
        def unpack_fn(bytes_):
            return struct.unpack(fmt, bytes_)[0]
    elif sampwidth == 4:
        fmt = '<i'
        def unpack_fn(bytes_):
            return struct.unpack(fmt, bytes_)[0]
    else:
        raise ValueError(f"Unsupported sample width: {sampwidth}")

    signal = np.zeros((n_frames * n_channels,), dtype=np.int32)
    byte_per_sample = sampwidth
    for i in range(n_frames * n_channels):
        bytes_ = data[i*byte_per_sample:(i+1)*byte_per_sample]
        signal[i] = unpack_fn(bytes_)
    return signal

def visualize_audio(file_name: str) -> None:
    data, frame_rate, n_frames, n_channels, sampwidth = AudioFileHandler.read_file_frate(file_name)

    signal = unpack_audio_data(data, n_frames, n_channels, sampwidth)

    if n_channels == 2:
        l_channel = signal[0::2]
        r_channel = signal[1::2]
    else:
        l_channel = signal

    l_channel_normalized = l_channel / np.max(np.abs(l_channel))

    cutoff_frequency = 5000
    l_channel_filtered = lowpass_filter(l_channel_normalized, cutoff_frequency, frame_rate)

    times = np.linspace(0, n_frames / frame_rate, num=n_frames)

    plt.figure(figsize=(15, 5))
    plt.title('Wav file signal (Filtered)')
    plt.xlabel("Time [s]")
    plt.ylabel("Normalized Amplitude")
    plt.plot(times, l_channel_filtered, alpha=0.7)
    plt.xlim(0, n_frames / frame_rate)
    plt.ylim(-1.1, 1.1)
    plt.show()

import numpy as np
from pathlib import WindowsPath, PosixPath

from scipy.stats import entropy as scipy_entropy

from src.cryptographer.model.audio_model import AudioFileHandler


def encryption_test(
        original: WindowsPath | PosixPath,
        encrypted: WindowsPath | PosixPath,
        decrypted: WindowsPath | PosixPath
) -> None:
    original_data, _ = AudioFileHandler.read_file(original)
    encrypted_data, _ = AudioFileHandler.read_file(encrypted)
    decrypted_data, _ = AudioFileHandler.read_file(decrypted)

    print("Entropy of original data:", calculate_entropy(original_data))
    print("Entropy of encrypted data:", calculate_entropy(encrypted_data))
    print("Entropy of decrypted data:", calculate_entropy(decrypted_data))


    original_data = np.frombuffer(original_data, dtype=np.int16)
    encrypted_data = np.frombuffer(encrypted_data, dtype=np.int16)
    decrypted_data = np.frombuffer(decrypted_data, dtype=np.int16)

    min_len = min(len(original_data), len(encrypted_data), len(decrypted_data))
    original_data = original_data[:min_len]
    encrypted_data = encrypted_data[:min_len]
    decrypted_data = decrypted_data[:min_len]

    noise_encrypted = encrypted_data - original_data
    noise_decrypted = decrypted_data - original_data

    snr_encrypted = calculate_snr(original_data, noise_encrypted)
    snr_decrypted = calculate_snr(original_data, noise_decrypted)

    print(f"SNR (Original vs Encrypted): {snr_encrypted} dB")
    print(f"SNR (Original vs Decrypted): {snr_decrypted} dB")


    original_data = np.frombuffer(original_data, dtype=np.int8)
    encrypted_data = np.frombuffer(encrypted_data, dtype=np.int8)
    decrypted_data = np.frombuffer(decrypted_data, dtype=np.int8)


    correlation_original_encrypted = calculate_correlation(original_data, encrypted_data)
    correlation_original_decrypted = calculate_correlation(original_data, decrypted_data)

    print(f"Correlation (Original vs Encrypted): {correlation_original_encrypted}")
    print(f"Correlation (Original vs Decrypted): {correlation_original_decrypted}")


def calculate_entropy(data):
    """Calculate the entropy of a byte array."""
    data_array = np.frombuffer(data, dtype=np.uint8)
    byte_counts = np.bincount(data_array, minlength=256)
    byte_probs = byte_counts / len(data_array)
    return scipy_entropy(byte_probs, base=2)

def calculate_snr(signal, noise):
    """Calculate the Signal-to-Noise Ratio (SNR) in dB."""
    signal_power = np.mean(signal ** 2)
    noise_power = np.mean(noise ** 2)

    if noise_power == 0:
        return float('inf') if signal_power > 0 else 0

    snr = 10 * np.log10(signal_power / noise_power)
    return snr

def calculate_correlation(data1, data2):
    """Calculate the Pearson correlation coefficient between two byte arrays."""
    return np.corrcoef(data1, data2)[0, 1]

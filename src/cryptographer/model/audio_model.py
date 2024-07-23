"""
This module provides functionalities for handling audio files, including reading from and writing to .wav files.

Classes
-------
AudioFileHandler
    A class used to read and write audio files in .wav format.

Methods
-------
read_file(file_path)
    Reads an audio file and returns the frames and parameters.
write_file(audio_data, file_path, params, key, format=".wav")
    Writes audio data to a file with specified parameters and key.
"""

from pathlib import WindowsPath, PosixPath
from logging import getLogger

import wave

from src.util import log_config

core_logger = getLogger('core')

class AudioFileHandler:
    """
    A class to handle reading and writing of audio files.

    ...

    Methods
    -------
    read_file(file_path)
        Reads an audio file and returns the frames and parameters.
    write_file(audio_data, file_path, params, key, format=".wav")
        Writes audio data to a file with specified parameters and key.
    """

    @staticmethod
    def read_file(file_path: WindowsPath | PosixPath) -> tuple[bytes, wave._wave_params]:
        """
        Reads an audio file and returns the frames and parameters.

        Parameters
        ----------
        file_path : WindowsPath or PosixPath
            The path to the input audio file.

        Returns
        -------
        tuple
            A tuple containing the audio frames (bytes) and the audio parameters (wave._wave_params).
        """
        with wave.open(str(file_path), 'rb') as audio:
            frames = audio.readframes(audio.getnframes())
            params = audio.getparams()
        return frames, params

    @staticmethod
    def write_file(
            audio_data: list,
            file_path: WindowsPath | PosixPath,
            params: wave._wave_params,
            key: str,
            format: str = ".wav"
    ) -> None:
        """
        Writes audio data to a file with specified parameters and key.

        Parameters
        ----------
        audio_data : list
            The audio data to be written to the file.
        file_path : WindowsPath or PosixPath
            The path to save the output audio file.
        params : wave._wave_params
            The parameters of the audio file.
        key : str
            The encryption/decryption key.
        format : str, optional
            The format of the output audio file (default is ".wav").

        Returns
        -------
        None
        """
        file_path: str = str(file_path)
        if not file_path.endswith(".wav"):
            file_path = f"{str(file_path)}{format}"
        with wave.open(file_path, 'wb') as decrypted_audio:
            decrypted_audio.setparams(params)
            decrypted_audio.writeframes(bytes(audio_data))
        core_logger.info(f"file was generated at {file_path} with the key {key}")
        return

    @staticmethod
    def read_file_frate(file_path: WindowsPath | PosixPath) -> tuple[bytes, int, int]:
        """
        Reads an audio file and returns the frames and parameters and framerate.

        Parameters
        ----------
        file_path : WindowsPath or PosixPath
            The path to the input audio file.

        Returns
        -------
        tuple
            A tuple containing the audio frames (bytes) and the audio parameters (wave._wave_params)
            and framerate.
        """
        with wave.open(str(file_path), 'rb') as audio:
            frames = audio.readframes(audio.getnframes())
            framerate = audio.getframerate()
            n_frames = audio.getnframes()
            n_channels = audio.getnchannels()
            sampwidth = audio.getsampwidth()
        return frames, framerate, n_frames, n_channels, sampwidth

    @staticmethod
    def inspect_wav(file_path):
        with wave.open(str(file_path), 'rb') as audio:
            print(f"Channels: {audio.getnchannels()}")
            print(f"Sample Width: {audio.getsampwidth()}")
            print(f"Frame Rate: {audio.getframerate()}")
            print(f"Number of Frames: {audio.getnframes()}")
            print(f"Parameters: {audio.getparams()}")

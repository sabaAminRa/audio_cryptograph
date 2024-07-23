"""
This module contains the Application class for handling audio file encryption and decryption.

Classes
-------
Application
    A class used to handle audio file encryption and decryption processes.
"""

from logging import getLogger
from pathlib import PosixPath, WindowsPath
from typing import Union, Optional

from src.util import log_config
from .controller.audio_controller import AudioController
from .model.audio_model import AudioFileHandler

core_logger = getLogger("core")


class Application:
    """
    A class to handle audio file encryption and decryption.

    Attributes
    ----------
    file_path : Union[WindowsPath, PosixPath]
        The path to the input audio file.
    out : Union[WindowsPath, PosixPath]
        The path to save the processed audio file.
    fast : bool
        Perform the operation faster with less security.
    key : Optional[str]
        The encryption/decryption key (default is None).

    Methods
    -------
    __init__(self, file_path, out, fast, key=None)
        Constructs the necessary attributes for the Application object and processes the audio file.
    """

    def __init__(
        self,
        file_path: Union[WindowsPath, PosixPath],
        out: Union[WindowsPath, PosixPath],
        fast: bool,
        key: Optional[str] = None,
    ) -> None:
        """
        Constructs the necessary attributes for the Application object and processes the audio file.

        Parameters
        ----------
        file_path : Union[WindowsPath, PosixPath]
            The path to the input audio file.
        out : Union[WindowsPath, PosixPath]
            The path to save the processed audio file.
        fast : bool
            Perform the operation faster with less security.
        key : Optional[str], optional
            The encryption/decryption key (default is None).

        Returns
        -------
        None
        """
        audio_bytes, params = AudioFileHandler.read_file(file_path)
        audio_controller = AudioController(audio_bytes)
        if key:
            core_logger.info(f"User requested to decrypt {file_path} with key {key}")
            data = audio_controller.decrypt(key, fast)
            AudioFileHandler.write_file(data, out, params, key)
            core_logger.info(f"{out} was generated")
        else:
            core_logger.info(f"User requested to encrypt {file_path}")
            data, key = audio_controller.encrypt(fast)
            AudioFileHandler.write_file(data, out, params, key)
            core_logger.info(f"{out} was generated with key {key}")

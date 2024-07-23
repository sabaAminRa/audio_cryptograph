"""
This module provides the AudioController class for handling the encryption and decryption of audio data.

Classes
-------
AudioController
    A class used to encrypt and decrypt audio data.
"""

from src.cryptographer.helper import (
    generate_key,
    seeded_shuffle,
    seeded_unshuffle,
    generate_chaotic_parameters,
    encrypt_key,
    decrypt_key,
    generate_logistic_map_seq,
    get_random_digits,
    encrypt_data_gcm,
    decrypt_data_gcm
)
from typing import Tuple, Union

class AudioController:
    """
    A class to handle the encryption and decryption of audio data.

    Methods
    -------
    __init__(self, audio_data: bytes) -> None
        Initializes the AudioController with audio data.
    encrypt(self, fast: bool) -> Tuple[Union[bytes, list[int]], str]
        Encrypts the audio data and returns the encrypted data and encryption key.
    decrypt(self, key: str, fast: bool) -> bytes
        Decrypts the audio data using the provided key and returns the decrypted data.
    """

    def __init__(self, audio_data: bytes) -> None:
        """
        Initializes the AudioController with audio data.

        Parameters
        ----------
        audio_data : bytes
            The audio data to be processed.

        Returns
        -------
        None
        """
        self.audio_data = audio_data

    def encrypt(self, fast: bool) -> Tuple[Union[bytes, list[int]], str]:
        """
        Encrypts the audio data and returns the encrypted data and encryption key.

        Parameters
        ----------
        fast : bool
            Flag to indicate if the encryption should be faster with less security.

        Returns
        -------
        Tuple[Union[bytes, list[int]], str]
            A tuple containing the encrypted audio data and the encryption key.
        """
        key = generate_key()
        r1, r2, x1, x2 = generate_chaotic_parameters(key)

        if not fast:
            chaotic_seq = generate_logistic_map_seq(r1, x1)
            seed = get_random_digits(chaotic_seq, key)
            self.audio_data = seeded_shuffle(self.audio_data, int(seed))

        chaotic_seq = generate_logistic_map_seq(r2, x2)
        gkey = get_random_digits(chaotic_seq, key)
        password, nonce, salt = gkey[:32], bytes(gkey[32:44], encoding='ascii'), bytes(gkey[44:], encoding='ascii')
        self.audio_data = encrypt_data_gcm(self.audio_data, password, nonce, salt)

        encrypted_key = encrypt_key(key)
        return self.audio_data, encrypted_key

    def decrypt(self, key: str, fast: bool) -> bytes:
        """
        Decrypts the audio data using the provided key and returns the decrypted data.

        Parameters
        ----------
        key : str
            The key used to decrypt the audio data.
        fast : bool
            Flag to indicate if the decryption should be faster with less security.

        Returns
        -------
        bytes
            The decrypted audio data.
        """
        key = decrypt_key(key)
        r1, r2, x1, x2 = generate_chaotic_parameters(key)

        chaotic_seq = generate_logistic_map_seq(r2, x2)
        gkey = get_random_digits(chaotic_seq, key)
        password, nonce, salt = gkey[:32], bytes(gkey[32:44], encoding='ascii'), bytes(gkey[44:], encoding='ascii')
        self.audio_data = decrypt_data_gcm(self.audio_data, password, nonce, salt)

        if not fast:
            chaotic_seq = generate_logistic_map_seq(r1, x1)
            seed = get_random_digits(chaotic_seq, key)
            self.audio_data = seeded_unshuffle(self.audio_data, int(seed))

        return self.audio_data

import os
import sys
from logging import getLogger
from secrets import SystemRandom
from cryptography.fernet import Fernet
from typing import Tuple

from .collatz import generate_collatz_sequence, map_to_chaotic_range
from src.util import config, log_config

logger = getLogger("core")

def generate_key() -> str:
    """
    Generates a random key for encryption or decryption.

    Returns
    -------
    str
        A randomly generated key as a string.
    """
    sys_random = SystemRandom()
    key = sys_random.randrange(1_000_000_000_000_00, 1_000_000_000_000_000)
    return str(key)

def encrypt_key(key: str) -> str:
    """
    Encrypts a key using Fernet encryption.

    Parameters
    ----------
    key : str
        The key to be encrypted.

    Returns
    -------
    str
        The encrypted key as a string.
    """
    fernet_key = os.environ.get('fkey', config.get_value('settings.encryption', 'fkey'))
    if not fernet_key:
        logger.info("Please set your encryption key in the setting or your environment as described in the README.md file")
        sys.exit(1)
    fernet = Fernet(fernet_key.encode())
    encrypted_key = fernet.encrypt(key.encode()).decode()
    return encrypted_key

def decrypt_key(encrypted_key: str) -> str:
    """
    Decrypts a key using Fernet encryption.

    Parameters
    ----------
    encrypted_key : str
        The key to be decrypted.

    Returns
    -------
    str
        The decrypted key as a string.
    """
    fernet_key = os.environ.get('fkey', config.get_value('settings.encryption', 'fkey'))
    if not fernet_key:
        logger.info("Please set your encryption key in the setting or your environment as described in the README.md file")
        sys.exit(1)
    fernet = Fernet(fernet_key.encode())
    try:
        key = fernet.decrypt(encrypted_key.encode()).decode()
    except Exception:
        logger.info(f"Invalid key, {fernet_key}")
        sys.exit(1)
    return key

def generate_chaotic_parameters(key: str) -> Tuple[float, float, float, float]:
    """
    Generates chaotic parameters based on a provided key for the encryption process.

    Parameters
    ----------
    key : str
        The key used to generate the seeds.

    Returns
    -------
    tuple of float
        A tuple containing four chaotic parameters generated from the key.
    """
    t, p, q, s = int(key[:7]), int(key[7:10]), int(key[10:13]), int(key[13:])

    r1 = generate_collatz_sequence(t + q, p) / 1e15
    r2 = generate_collatz_sequence(t + p, q) / 1e15
    x1 = generate_collatz_sequence(t + q, p - s) / 1e15
    x2 = generate_collatz_sequence(t + p, p + s) / 1e15

    r1 = map_to_chaotic_range(r2)
    r2 = map_to_chaotic_range(r2)

    return r1, r2, x1, x2

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def encrypt_data_gcm(data: bytes, password: str, nonce: bytes, salt: bytes) -> bytes:
    """
    Encrypts data using AES-GCM with a password-derived key.

    Parameters
    ----------
    data : bytes
        The data to be encrypted.
    password : str
        The password to derive the encryption key.
    nonce : bytes
        The nonce to use for the AES-GCM mode.
    salt : bytes
        The salt to use for key derivation.

    Returns
    -------
    bytes
        The encrypted data.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())

    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data)
    return encrypted_data

def decrypt_data_gcm(data: bytes, password: str, nonce: bytes, salt: bytes) -> bytes:
    """
    Decrypts data using AES-GCM with a password-derived key.

    Parameters
    ----------
    data : bytes
        The encrypted data to be decrypted.
    password : str
        The password to derive the decryption key.
    nonce : bytes
        The nonce used for the AES-GCM mode.
    salt : bytes
        The salt used for key derivation.

    Returns
    -------
    bytes
        The decrypted data.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())

    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_data = decryptor.update(data)
    return decrypted_data

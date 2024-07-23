from typing_extensions import Annotated
from pathlib import Path
import logging

logging.getLogger('matplotlib').setLevel(logging.ERROR)
logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)

import matplotlib as mpl
import typer

from src.cryptographer.application import Application
from src.test import (
    visualize_audio,
    generate_random_sequence,
    encryption_test
)

mpl.set_loglevel('warning')

app = typer.Typer()

@app.command(help="Encrypt .wav audio file, input file and output file are required, generates encrypted file + key")
def encrypt(
    file: Annotated[
        Path,
        typer.Option(
            "--in", "-i",
            help="The file to encrypt",
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        )
    ],
    out: Annotated[
        Path,
        typer.Option(
            "--out", "-o",
            help="The name of the encrypted file that will be generated",
            exists=False,
            dir_okay=True,
            writable=True,
            resolve_path=True
        )
    ],
    fast: Annotated[bool, typer.Option("--fast", "-f",
        help="Perform Encryption faster without shuffling, suited for large files")] = False
) -> None:
    """
    Encrypts an audio file and saves the encrypted file to the specified output path.

    Parameters
    ----------
    file : Path
        The path to the input audio file. Must exist and be readable.
    out : Path
        The path to save the encrypted audio file. Must not exist but the directory should be writable.
    fast : bool, optional
        Perform encryption faster with less security, by default False.

    Returns
    -------
    None
    """
    application = Application(file, out, fast)

@app.command(help="Decrypt .wav audio file, input file, output file and key are required")
def decrypt(
    file: Annotated[
        Path,
        typer.Option(
            "--in", "-i",
            help="Name of the encrypted file that needs to decrypted",
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        )
    ],
    out: Annotated[
        Path,
        typer.Option(
            "--out", "-o",
            help="Name of the decrypted file, that will be generated",
            exists=False,
            dir_okay=True,
            writable=True,
            resolve_path=True
        )
    ],
    key: Annotated[str, typer.Option("--key", "-k")],
    fast: Annotated[bool, typer.Option(
        "--fast", "-f",
        help="Perform decryption faster without unshuffling, only works if encryption was also done with the --fast switch")] = False
) -> None:
    """
    Decrypts an audio file using the provided key and saves the decrypted file to the specified output path.

    Parameters
    ----------
    file : Path
        The path to the input audio file. Must exist and be readable.
    out : Path
        The path to save the decrypted audio file. Must not exist but the directory should be writable.
    key : str
        The key to use for decrypting the audio file.
    fast : bool, optional
        Perform decryption faster with less security, only works if encryption was also done with the --fast switch. By default False.

    Returns
    -------
    None
    """
    application = Application(file, out, fast, key=key)


@app.command(help="Make a plot of an audio file, audio signal / time")
def plot(
    file: Annotated[
        Path,
        typer.Option(
            "--file", "-f",
            help="Audio file name that is being ploted",
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        )
    ],
) -> None:
     visualize_audio(file)


@app.command(help="Test Correlation, Signal to noise ratio and entropy of encryption/decryption proccess")
def test(
    original: Annotated[
        Path,
        typer.Option(
            "--original", "-o",
            help="The original file",
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        )
    ],
    encrypted: Annotated[
        Path,
        typer.Option(
            "--encrypted", "-e",
            help="The encrypted file",
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        )
    ],
    decrypted: Annotated[
        Path,
        typer.Option(
            "--decrypted", "-d",
            help="The decrypted file",
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        )
    ],

) -> None:
    encryption_test(original, encrypted, decrypted)


@app.command(help="generates 10 binary data files suitable for NIST test based on collatz conjecture sequence")
def nist() -> None:
    generate_random_sequence()


if __name__ == "__main__":
    app()

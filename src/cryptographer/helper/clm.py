import random
from typing import Optional

def generate_logistic_map_seq(r1: float, x1: float, n: int = 10_000) -> str:
    """
    Generates a sequence based on the logistic map.

    Parameters
    ----------
    r1 : float
        The control parameter for the logistic map.
    x1 : float
        The initial value for the logistic map.
    n : int, optional
        The number of iterations to perform (default is 10,000).

    Returns
    -------
    str
        The generated logistic map sequence.
    """
    logistic_map_key = ''
    for _ in range(n):
        x1 = x1 * r1 * (1 - x1)
        logistic_map_key += str(x1)[-1]
    return logistic_map_key


def map_to_chaotic_range(value: float, lower: float = 3.57, upper: float = 4.00) -> float:
    """
    Maps a value to a chaotic range.

    Parameters
    ----------
    value : float
        The value to map.
    lower : float, optional
        The lower bound of the chaotic range (default is 3.57).
    upper : float, optional
        The upper bound of the chaotic range (default is 4.00).

    Returns
    -------
    float
        The mapped value within the chaotic range.
    """
    return lower + (upper - lower) * value


def get_random_digits(chaotic_seq: str, key: str) -> str:
    """
    Generates a string of random digits based on a chaotic sequence and a key.

    Parameters
    ----------
    chaotic_seq : str
        The chaotic sequence to select digits from.
    key : str
        The key to seed the random number generator.

    Returns
    -------
    str
        A string of 60 random digits selected from the chaotic sequence.
    """
    random_digits = ''
    rand = random.Random(key)
    for _ in range(60):
        chosen = rand.choice(chaotic_seq)
        random_digits += chosen
    return random_digits

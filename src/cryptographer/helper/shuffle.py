import random

def seeded_shuffle(audio_data: list | bytes, seed: int) -> bytes:
    """
    Shuffles audio data based on a provided seed.

    Parameters
    ----------
    audio_data : list or bytes
        The audio data to be shuffled.
    seed : int
        The seed for the random number generator.

    Returns
    -------
    list
        The shuffled audio data.
    """
    rng = random.Random(seed)
    if not type(audio_data) == list: audio_data = list(audio_data)
    for i in range(len(audio_data) - 1, -1, -1):
        j = rng.randint(0, i)
        audio_data[i], audio_data[j] = audio_data[j], audio_data[i]
    return bytes(audio_data)

def seeded_unshuffle(audio_data: list | bytes, seed: int) -> bytes:
    """
    Unshuffles audio data based on a provided seed.

    Parameters
    ----------
    audio_data : list or bytes
        The audio data to be unshuffled.
    seed : int
        The seed for the random number generator.

    Returns
    -------
    list
        The unshuffled audio data.
    """
    rng = random.Random(seed)
    if not type(audio_data) == list: audio_data = list(audio_data)
    indices = [rng.randint(0, i) for i in range(len(audio_data) - 1, -1, -1)]
    for i, j in enumerate(indices[::-1]):
        audio_data[i], audio_data[j] = audio_data[j], audio_data[i]
    return bytes(audio_data)

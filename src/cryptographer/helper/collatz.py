def generate_collatz_sequence(n: int, start_index: int) -> int:
    """
    Generates a sequence of digits from the Collatz sequence starting from a given index.

    Parameters
    ----------
    n : int
        The starting number for the Collatz sequence.
    start_index : int
        The index from which to start extracting digits from the Collatz sequence.

    Returns
    -------
    int
        A 15-digit integer extracted from the Collatz sequence starting from the given index.
    """
    sequence = ""
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        sequence += str(n)

    # Ensure the start_index is within bounds
    if start_index > len(sequence) - 15:
        start_index = max(0, len(sequence) - 15)

    sequence = sequence[start_index:start_index + 15]
    return int(sequence)

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

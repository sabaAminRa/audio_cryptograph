from secrets import SystemRandom

from src.util import BASE_DIR

def generate_random_sequence() -> int:
    sys_random = SystemRandom()
    for i in range(10):
        key = str(sys_random.randrange(1_000_000_000_000_00, 1_000_000_000_000_000))
        n = int(key[:7])
        file_name = str(BASE_DIR.parent / f"binary_sequence{i}.txt")
        sequence = ""
        while n != 1:
            if n % 2 == 0:
                n = n // 2
            else:
                n = 3 * n + 1
            sequence += str(n)[-1]
        binary_sequence = ''.join(format(int(digit), '04b') for digit in sequence)
        with open(file_name, 'w') as file:
            file.write(binary_sequence)

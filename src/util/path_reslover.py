from pathlib import Path

__ALL__ = ['BASE_DIR']

def get_base_dir() -> Path:
    return Path(__file__).parent.parent.resolve()

BASE_DIR = get_base_dir()

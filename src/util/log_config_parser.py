from logging.config import fileConfig

from .path_reslover import BASE_DIR
from .config_parser import config
from .funcs import create_directories


def get_log_config():
    create_directories(BASE_DIR, ("logs",))
    return fileConfig(BASE_DIR / config.get_value("settings.log", "LOG_CONFIG"))

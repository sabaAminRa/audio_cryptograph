from .config_parser import config
from .log_config_parser import get_log_config
from .path_reslover import BASE_DIR


__ALL__ = ['config', 'log_config', 'BASE_DIR']

log_config = get_log_config()

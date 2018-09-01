import logging
from os import environ
from os.path import expanduser

import yaml


logger = logging.getLogger(__name__)


_DEFAULT_CONFIG = {
    'hostname': None,
    'plugins': [
        'hostname',
        'ip',
        'uptime',
	'load',
        'mem_usage',
        'swap_usage',
    ]
}

_DEFAULT_CONFIG_LOCATION = expanduser('~/.config/dsb/dsb.yml')
_CONFIG_LOCATION = environ.get('DSB_CONFIG', _DEFAULT_CONFIG_LOCATION)

config = _DEFAULT_CONFIG

try:
    with open(_CONFIG_LOCATION) as f:
        config = yaml.load(f.read())
        logger.info(f'Using config file { _CONFIG_LOCATION }')

except FileNotFoundError:
    logger.warn(f'Config file not found ({ _CONFIG_LOCATION }). Using default config')

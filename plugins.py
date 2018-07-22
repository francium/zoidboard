from contextlib import contextmanager
from datetime import datetime
import importlib
import logging
import os
import re
import sys
from typing import Dict, Callable

from utils import run_cmd    


CUSTOM_PLUGIN_LOCATION = os.path.expanduser('~/.config/dsb/plugins/')

logger = logging.getLogger()


def _hostname() -> str:
    return 'Hostname', run_cmd('cat', '/etc/hostname')


def _ip() -> str:
    return 'IP', run_cmd('hostname', '-i').split(' ')[0]


def _mem() -> Dict[str, int]:
    raw_lines = run_cmd('cat', '/proc/meminfo').split('\n')[:-1]
    col_lines = [list(filter(bool, re.split('\s', line)))
                    for line in raw_lines]
    data = {cols[0][:-1]: int(cols[1]) for cols in col_lines}
    return 'Memory', f"{ round(data['MemTotal'] / 1024, 1) } MiB"
    # { 'total':     round(data['MemTotal'] / 1024, 1),
    #   'active':    round(data['Active'] / 1024, 1),
    #   'free':      round(data['MemFree'] / 1024, 1),
    #   'available': round(data['MemAvailable'] / 1024, 1),
    #   'buffers':   round(data['Buffers'] / 1024, 1),
    #   'cached':    round(data['Cached'] / 1024, 1) }


def _uptime() -> str:
    uptime = run_cmd('cat', '/proc/uptime').split(' ')[0]
    now = datetime.now()
    then = datetime.fromtimestamp(now.timestamp() - float(uptime))
    # Decimal points from timedelta are split out
    return 'Uptime', str(now - then).split('.')[0]


def _temp() -> float:
    return 'Temperature', 33.3


# def get_stats_disk_active
# pat = re.compile('^sd[a-z]', re.M)
# re.findall(pat, string)


@contextmanager
def _load_custom_plugin_safe(plugin_name):
    sys.path.append(CUSTOM_PLUGIN_LOCATION)
    try:
        logger.debug(f'Loading custom plugin: { plugin_name }')
        plugin_module = importlib.import_module(plugin_name)

        if not hasattr(plugin_module, 'plugin'):
            logger.warn('Plugin module is invalid. Plugin modules must provide'
                        'a "plugin" function')
            yield None

        yield plugin_module.plugin
    except ModuleNotFoundError:
        logger.warn(f'Could not find plugin ({ plugin_name }) in plugin'
                    f' directory ({ CUSTOM_PLUGIN_LOCATION })')
        yield None

    sys.path.remove(CUSTOM_PLUGIN_LOCATION)


def _load_custom_plugin(plugin_name: str):
    with _load_custom_plugin_safe(plugin_name) as plugin:
        return plugin


mapping = {
    'hostname': _hostname,
    'ip': _ip,
    'uptime': _uptime,
    'memory': _mem,
    'cpu_temp': _temp
}


def get(plugin_name: str) -> Callable:
    plugin = mapping.get(plugin_name)
    if plugin: 
        logger.debug('Returning builtin plugin')
        return plugin

    custom_plugin = _load_custom_plugin(plugin_name)
    logger.warn(f'Custom plugin: {custom_plugin}')
    if custom_plugin: 
        logger.debug('Returning custom plugin')
        return custom_plugin

    return (lambda: (None, None))
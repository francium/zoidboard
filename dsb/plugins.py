from contextlib import contextmanager
from datetime import datetime
import importlib
import logging
import os
import re
import sys
from typing import Dict, Callable, Union


CUSTOM_PLUGIN_LOCATION = os.path.expanduser('~/.config/dsb/plugins/')


logger = logging.getLogger()

cache = {}


@contextmanager
def _try_import(name: str, custom_location: Union[str] = None):
    if custom_location: sys.path.append(CUSTOM_PLUGIN_LOCATION)

    try:
        logger.debug(f'Try to import module "{ name }"')
        yield importlib.import_module(name)
    except ModuleNotFoundError:
        logger.debug(f'Could not find module "{ name }"')
        yield None

    if custom_location: sys.path.remove(CUSTOM_PLUGIN_LOCATION)


def _load_builtin_plugin(plugin_name: str):
    with _try_import('dsb.builtin_plugins.' + plugin_name) as plugin:
        if plugin:
            logger.debug(f'Loaded builtin plugin "{ plugin_name }"')
        else:
            logger.warn(f'Could not find buitlin plugin "{ plugin_name }"')

        return plugin


def _load_custom_plugin(plugin_name: str):
    with _try_import(plugin_name, CUSTOM_PLUGIN_LOCATION) as plugin:
        if plugin:
            logger.debug(f'Loaded custom plugin "{plugin_name }"')
        else:
            logger.warn(f'Could not find plugin "{ plugin_name }" in plugin'
                        f' directory "{ CUSTOM_PLUGIN_LOCATION }"')
        return plugin


def get(plugin_name: str) -> Union[Callable]:
    cached = cache.get(plugin_name)
    found = _load_builtin_plugin(plugin_name) or _load_custom_plugin(plugin_name)
    if not cached and found:
        cache[plugin_name] = found

    return cached or found


def serialize_plugin(name, plugin):
    return {'name': name,
            'plugin': {'label': plugin.label,
                       'update_period': plugin.update_period,
                       'typeof': (plugin.typeof[0], str(plugin.typeof[1])),
                       'units': plugin.units}}

import datetime
import logging
import re
import subprocess as sp
from typing import Dict
import threading

from zoidboard.config import config
from zoidboard.runner import Plugin, PluginRunner
from zoidboard.store import store
from zoidboard.app import create_app
from zoidboard.plugins import get as get_plugin


logger = logging.getLogger(__name__)


def main():
    plugins = {}
    for plugin_name in config['plugins']:
        plugin = get_plugin(plugin_name)
        if not plugin: continue

        plugins[plugin_name] = Plugin.from_module(plugin)

    logger.info('Starting zoidboard')
    runner = PluginRunner(plugins)
    logger.info(f'runner: {runner}')
    runner_thread = threading.Thread(target=runner.start)
    runner_thread.start()

    logger.info(f'started runner thread')

    app = create_app(plugins)
    app_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0'})
    app_thread.start()

    app_thread.join()
    runner_thread.join()


if __name__ == '__main__':
    main()

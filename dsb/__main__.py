import datetime
import logging
import re
import subprocess as sp
from typing import Dict
import threading

from dsb.config import config
from dsb.runner import Plugin, PluginRunner
from dsb.store import store
from dsb.app import create_app
from dsb.plugins import get as get_plugin


logger = logging.getLogger(__name__)

plugins = []
for plugin_name in config['plugins']:
    plugin = get_plugin(plugin_name)
    if not plugin: continue

    plugins.append(Plugin.from_module(plugin))

runner = PluginRunner(plugins)
thread = threading.Thread(target=runner.start)
thread.start()

app = create_app(plugins)
app.run(debug=True)
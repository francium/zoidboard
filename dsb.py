import __logging__

import datetime
import logging
import re
import subprocess as sp
from typing import Dict

from flask import Flask, render_template

from config import config
import plugins
from utils import run_cmd


logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/')
def route_index():
    stats = get_stats()
    return render_template('index.html', stats=stats)


def get_stats():
    stats = []
    for plugin_name in config['plugins']:
        logger.debug(f'Loading plugin: { plugin_name }')
        label, value = plugins.get(plugin_name)()
        if not label and not value:
            logger.warn(f'Plugin not found: { plugin_name }')
            continue

        logger.debug(f'Add plugin value to results: ({ label, value })')
        stats.append({ 'label': label, 'value': value })

    return stats
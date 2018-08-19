import json
import logging
from typing import List

from flask import Flask, render_template, request
from flask_cors import CORS

from .config import config
from .plugins import get as get_plugin, serialize_plugin
from .store import store


logger = logging.getLogger()


def create_app(plugins):
    app = Flask(__name__)
    CORS(app)

    @app.route('/')
    def route_index():
        return render_template('index.html')

    @app.route('/api/plugin/registered')
    def rotue_api_registered_plugins():
        return json.dumps(config['plugins'])

    @app.route('/api/plugin/schemas')
    def route_api_plugin_schemas():
        plugins: List[str] = config['plugins']
        return _get_plugin_schemas(plugins)

    @app.route('/api/plugin/stats')
    def route_api_stats():
        plugins: str = config['plugins']
        return _get_stats(plugins)

    app.logger.setLevel(logging.ERROR)
    return app


def _get_stats(plugins: List[str]):
    stats = []
    for name in plugins:
        data = store.get(name)
        stats.append({'name': name,
                      'data': data})

    return json.dumps(stats)


def _get_plugin_schemas(plugin_names: List[str]):
    names_and_plugins = [(name, get_plugin(name)) for name in plugin_names]
    schemas = [serialize_plugin(name, plugin) for name, plugin in names_and_plugins]
    return json.dumps(list(schemas))

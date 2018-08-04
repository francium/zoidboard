from flask import Flask, render_template

from .store import store


def create_app(plugins):
    app = Flask(__name__)

    @app.route('/')
    def route_index():
        stats = get_stats()
        return render_template('index.html', stats=stats)

    def get_stats():
        stats = []
        for plugin in plugins:
            data = store.get(plugin.label)
            stats.append((plugin.label, data))
        return stats

    return app
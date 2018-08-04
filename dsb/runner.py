# TODO
#   - clean up pool when exiting

from multiprocessing.dummy import Pool
import time
from typing import Any, Callable, List, Tuple, Union
import logging

from .scheduler import ScheduleItem, Scheduler
from .store import store
from .utils import run_cmd


logger = logging.getLogger()


class Plugin:
    def __init__(self,
                 label: str,
                 cmd: Callable,
                 callback: Callable,
                 update_period: Union[int],
                 units: Union[str],
                 typeof: Tuple[str, Any]):
        """
        :param label:
        :param call:
        :param callback:
        :param update_period:
        :param units:
        :param typeof:
        """
        self.label = label
        self.cmd = cmd
        self.callback = callback
        self.update_period = update_period
        self.next_run = -1
        self.units = units
        self.typeof = typeof

    def __lt__(self, that):
        return self

    def __gt__(self, that):
        return self

    def __str__(self):
        return f'<{self.label} ({self.update_period})>'

    @classmethod
    def from_module(cls, module):
        return cls(module.label, module.cmd, module.callback,
                   module.update_period, module.units, module.typeof)


class PluginRunner:
    TIMEOUT_DELTA = 0.05

    def __init__(self, plugins: List[Plugin]):
        self._plugins = plugins
        self._scheduler = Scheduler()
        self._exec_pool = Pool()
        self._t0 = 0

    def start(self):
        for plugin in self._plugins:
            data_points = getattr(plugin, 'data_points', None)
            store.register(plugin.label, plugin.typeof[0], data_points)
            self._scheduler.push((plugin.next_run, plugin))
        self.loop()

    def loop(self):
        while True:
            self._t0 = time.time()

            plugin = self._scheduler.get_next()[1]
            logger.debug(f'Next plugin: {plugin}')

            if (plugin.next_run > self._t0):
                sleep_time = plugin.next_run - self._t0
                logger.debug(f'Sleeping for {sleep_time}')
                time.sleep(sleep_time)

            self._submit_plugin(plugin)

    def _on_plugin_result(self, result: Any, plugin: Plugin):
        store.update(plugin.label, result)

    def _on_plugin_err(self, exc: Exception, plugin: Plugin):
        logger.warn(f'Plugin "{plugin.label}" failed with: {exc}')

    def _submit_plugin(self, plugin: Plugin):
        """Submit a plugin to execution pool and schedule its next run
        """
        self._exec_pool.apply_async(
            lambda: self._run_plugin(plugin),
            [],
            callback=self.partial(self._on_plugin_result, plugin),
            error_callback=self.partial(self._on_plugin_err, plugin))

        next_run = time.time() + plugin.update_period
        plugin.next_run = next_run
        item = next_run, plugin
        self._scheduler.push(item)

    @classmethod
    def _run_plugin(cls, plugin: Plugin) -> Any:
        """Callback for running a plugin
        """
        logger.debug(f'Running plugin "{plugin}"')
        result = run_cmd(*plugin.cmd,
                         timeout=plugin.update_period - cls.TIMEOUT_DELTA)
        return plugin.callback(result)

    def partial(self, callback: Callable, plugin):
        """`callback` is an instance method. `self` is implicitly passed in as
        the first argument
        """
        return lambda result_or_exc: callback(result_or_exc, plugin)


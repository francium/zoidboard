import json
import logging
import time
from threading import Thread
from typing import Any, List, Union


logger = logging.getLogger(__name__)

Timestamp = int


class _EMPTY:
    def __repr__(self): return '<EMPTY>'
_EMPTY = _EMPTY()


class RingerBuffer:
    def __init__(self, maxsize: int):
        self._buffer = [_EMPTY] * maxsize
        self._ptr = 0

    def push(self, item: Any) -> Union[Any]:
        self._buffer[self._ptr] = item
        self._ptr = (self._ptr + 1) % len(self._buffer)

    def read(self) -> List[Any]:
        buf = []
        for i in range(len(self._buffer)):
            item_index = (i + self._ptr) % len(self._buffer)
            item = self._buffer[item_index]
            if item is _EMPTY:
                continue

            buf.append(item)
        return buf


class Store:
    _PERSIST_INTERVAL = 60 * 0.5 # 5 minutes

    def __init__(self):
        self._data_last_persist: Dict[str, Union[Timestamp]] = {}
        self._data_map = {}
        self._persistance = StorePersistance()

    def register(self, label: str, typeof: str, maxsize=3600):
        maxsize = maxsize or 3600

        if typeof == 'scalar':
            value = 'scalar', None
        elif typeof == 'vector':
            value = 'vector', RingerBuffer(maxsize)
            data = self._load_persisted_data(label)
            for datum in data:
                value[1].push(datum)
        else:
            raise TypeError(f'typeof <{typeof}> is invalid')

        self._data_map[label] = value
        self._data_last_persist[label] = int(time.time())

    def update(self, label, value):
        entry = self._data_map.get(label)
        if not entry:
            raise LookupError(f'{label} not registered')

        typeof, data = entry
        if typeof == 'scalar':
            self._data_map[label] = typeof, value
        else:
            data.push(value)
        self._update_persistance(label, typeof)

    def get(self, label):
        entry = self._data_map.get(label)
        if not entry:
            raise LookupError(f'{label} not registered')

        typeof, data = entry
        return data if typeof == 'scalar' else data.read()

    def _update_persistance(self, label: str, typeof: str):
        if typeof == 'scalar': return

        time_now = int(time.time())
        last_persist = self._data_last_persist[label]
        secs_since_last_persist = None if last_persist is None \
                                      else time_now - last_persist

        if last_persist is None or secs_since_last_persist > self._PERSIST_INTERVAL:
            logger.info(f'Updating persistance for {label}')
            self._data_last_persist[label] = int(time.time())
            data = self.get(label)
            self._persistance.put(label, data)
        else:
            logger.debug(f'Skipping persistance upate for {label}: '
                         f'last_persist: {last_persist}, '
                         f'secs_since_last_persist: {secs_since_last_persist}')

    def _load_persisted_data(self, label: str):
        return self._persistance.get(label)


class StorePersistance:
    def get(self, label):
        try:
            with open(label + '.dat') as f:
                data = json.loads(f.read())
        except FileNotFoundError:
            logger.info(f'No existing data for {label + ".dat"}')
            return []

        logger.debug(f'Loading data for {label}: {data}')
        return data

    def put(self, label, data):
        logger.debug(f'Writing data to {label}: {data}')
        filename = label + '.dat'
        thread = Thread(target=self._write, args=(filename, data))
        thread.start()

    def _write(self, filename, data):
        with open(filename, 'w') as f:
            f.write(json.dumps(data))


store = Store()

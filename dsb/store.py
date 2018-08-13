from typing import Any, List, Union

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
    def __init__(self):
        self._map = {}

    def register(self, label, typeof, maxsize=3600):
        maxsize = maxsize or 3600

        if typeof == 'scalar':
            value = 'scalar', None
        elif typeof == 'vector':
            value = 'vector', RingerBuffer(maxsize)
        else:
            raise TypeError(f'typeof <{typeof}> is invalid')

        self._map[label] = value

    def update(self, label, value):
        entry = self._map.get(label)
        if not entry:
            raise LookupError(f'{label} not registered')

        typeof, data = entry
        if typeof == 'scalar':
            self._map[label] = typeof, value
        else:
            data.push(value)

    def get(self, label):
        entry = self._map.get(label)
        if not entry:
            raise LookupError(f'{label} not registered')

        typeof, data = entry

        if typeof == 'scalar':
            return data
        else:
            return data.read()


store = Store()

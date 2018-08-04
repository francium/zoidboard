import re
from typing import Dict


label = 'Memory Usage'
update_period = 1
data_points = int(24 * 3600 / update_period)
units = None
typeof = 'vector', float
cmd = 'cat', '/proc/meminfo'
def callback(result: str) -> Dict[str, int]:
    raw_lines = result.split('\n')[:-1]
    col_lines = [list(filter(bool, re.split('\s', line)))
                    for line in raw_lines]
    data = {cols[0][:-1]: int(cols[1]) for cols in col_lines}

    total = data['MemTotal']
    free = data['MemFree']
    buffers = data['Buffers']
    cached = data['Cached']
    used = total - free - buffers - cached

    return used / total
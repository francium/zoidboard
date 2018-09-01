label = 'Load'
update_period = 10
units = None
typeof = 'scalar', 'string'
cmd = 'cat', '/proc/loadavg'
def callback(result: str) -> str:
    labels = '1 min', '5 mins', '10 mins', 'processes'
    col_width = max([len(label) for label in labels])j
    # Don't care about last process id used (col 5)
    values = result.split(' ')[:-1]

    format_string = f'{{value:{col_width}.{col_width}s}}'
    labels_row = [format_string.format(value=label) for label in labels]
    values_row = [format_string.format(value=value) for value in values]

    return '  '.join(labels_row) + '\n' + '  '.join(values_row)

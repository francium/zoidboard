label = 'Hostname'
update_period = 99999
units = None
typeof = 'scalar', 'string'
cmd = 'cat', '/etc/hostname'
def callback(result: str) -> str:
    return result

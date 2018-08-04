label = 'Hostname'
update_period = 2
units = None
typeof = 'scalar', str
cmd = 'cat', '/etc/hostname'
def callback(result: str) -> str:
    return result
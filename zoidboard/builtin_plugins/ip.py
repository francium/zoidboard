label = 'IP Address'
update_period = 600
units = None
typeof = 'scalar', 'string'
cmd = 'hostname', '-i'
def callback(result: str) -> str:
    return result.split(' ')[0]

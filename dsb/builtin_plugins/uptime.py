from datetime import datetime


label = 'Uptime'
update_period = 5
units = None
typeof = 'scalar', str
cmd = 'cat', '/proc/uptime'
def callback(result: str) -> str:
    uptime = result.split(' ')[0]
    now = datetime.now()
    then = datetime.fromtimestamp(now.timestamp() - float(uptime))
    # Decimal points from timedelta are split out
    return str(now - then).split('.')[0]
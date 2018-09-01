from os import environ
import logging


log_format='%(asctime)s.%(msecs)03d %(levelname)8s [%(module)s %(funcName)s] %(message)s'
datefmt="%Y-%m-%d %H:%M:%S"
logger_level = logging.DEBUG if environ.get('DEBUG') else logging.INFO
logging.basicConfig(level=logger_level, format=log_format, datefmt=datefmt)

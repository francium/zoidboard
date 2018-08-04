from os import environ
import logging


logger_level = logging.DEBUG if environ.get('DSB_DEBUG') else logging.INFO
logging.basicConfig(level=logger_level)
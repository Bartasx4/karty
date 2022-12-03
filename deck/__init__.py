

__title__ = 'deck'
__author__ = 'Bartosz Szymanski'
__license__ = 'MIT'
__copyright__ = 'Copyright 2022 Bartosz Szymanski'
__version__ = '0.1.0'

import logging
import logging.config
from os import path
log_file_name = 'logging.conf'
log_file_path = path.join(path.dirname(path.abspath(__file__)), log_file_name)
logging.config.fileConfig(log_file_path, disable_existing_loggers=True)

from .errors import *
from .deck import Deck
from .card import Card
from .player import Player
from .playersgroup import PlayersGroup


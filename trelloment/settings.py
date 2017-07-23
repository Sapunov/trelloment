"""Trelloment settings file.
"""

import os
import json


NAME = 'trelloment'
BASE_DIR = os.path.join(os.path.sep, 'opt', NAME)
CONFIGS_DIR = os.path.join(os.path.sep, 'etc', NAME)

CREDENTIALS_FILENAME = os.path.join(CONFIGS_DIR, 'credentials.json')
CREDENTIALS = {}


if os.path.exists(CREDENTIALS_FILENAME):
    with open(CREDENTIALS_FILENAME) as credentials_file:
        CREDENTIALS = json.load(credentials_file)
else:
    raise FileNotFoundError('No credentials file')


HISTORY_PATH = os.path.join(BASE_DIR, 'history')

BOARDS_FILENAME = os.path.join(CONFIGS_DIR, 'boards')

BOARDS_TO_FOLLOW = []

if os.path.exists(BOARDS_FILENAME):
    with open(BOARDS_FILENAME) as boards_file:
        BOARDS_TO_FOLLOW = [bid.strip() for bid in boards_file.read().split()]


DONE_LIST = 'done'

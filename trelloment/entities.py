'''Trelloment entity specific functions.
'''

import os

from trelloment import settings
from trelloment import structures


def list_boards_ids():

    return os.listdir(os.path.join(settings.HISTORY_PATH, 'board'))


def list_cards_ids():

    return os.listdir(os.path.join(settings.HISTORY_PATH, 'card'))


def get_boards():

    return [structures.Board(board_id) for board_id in list_boards_ids()]


def get_cards():

    return [structures.Card(card_id) for card_id in list_cards_ids()]

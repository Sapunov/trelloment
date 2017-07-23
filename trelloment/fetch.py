"""Trelloment fetcher.
"""

import os

from trello import TrelloClient

from trelloment import common
from trelloment import core
from trelloment import settings


log = core.setup_log(__name__)


def get_card_data(card):

    checklists = card.fetch_checklists()

    data = {
        'id': card.id,
        'name': card.name,
        'todo_list': [],
        'todo': 0,
        'done': 0,
        'is_completed': False
    }

    if checklists:
        for todo in checklists[0].items:
            data['todo_list'].append(
                {
                    'id': todo['id'],
                    'name': todo['name'],
                    'is_completed': todo['checked']
                }
            )

        data['todo'] = len(data['todo_list'])
        data['done'] = sum(1 for todo in data['todo_list'] if todo['is_completed'])

        data['is_completed'] = True if data['todo'] == data['done'] else False
    else:
        # When card have no checklist than card have only
        # one task - to complete itself i.e. only one todo.
        #
        # In this case only list where card locates matter(`done` or another)
        if common.lower_eq(card.get_list().name, settings.DONE_LIST):
            data['is_completed'] = True

    return data


def get_board_data(board_id):

    client = TrelloClient(**settings.CREDENTIALS)

    board = client.get_board(board_id)
    cards = board.get_cards()

    data = {
        'id': board_id,
        'name': board.name,
        'cards': [],
        'todo': 0,
        'done': 0
    }

    for card in cards:
        data['cards'].append(get_card_data(card))

    if cards:
        data['todo'] = sum(1 for card in data['cards'] if not card['is_completed'])
        data['done'] = sum(1 for card in data['cards'] if card['is_completed'])

    return data


def save_current_state():

    log.debug('Start saving current boards state')

    boards_processed = 0

    for board_id in settings.BOARDS_TO_FOLLOW:
        log.debug('Start processing board<%s>', board_id)

        board_data = get_board_data(board_id)

        directory = os.path.join(settings.HISTORY_PATH, board_id)
        common.ensure_directory(directory)
        filepath = os.path.join(directory, common.get_today_string())
        common.save_data(board_data, filepath)

        log.debug('Board<%s> data saved to %s', board_id, filepath)

        boards_processed += 1

    log.debug('%s was processed')

    return boards_processed

"""Trelloment fetcher.
"""

import os

from trello import TrelloClient

from trelloment import settings
from trelloment import common


def get_card_data(card):

    checklists = card.fetch_checklists()

    data = {
        'id': card.id,
        'name': card.name,
        'todo_list': []
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
        data['done'] = sum(
            1 for todo in data['todo_list'] if todo['is_completed']
        )
    else:
        # When card have no checklist than card have only
        # one task - to complete itself i.e. only one todo.
        # In this case only list where card locats matter(`done` or another)
        data['todo'] = 1

        if common.lower_eq(card.get_list().name, settings.DONE_LIST):
            data['done'] = 1
        else:
            data['done'] = 0

    data['is_completed'] = True if data['todo'] == data['done'] else False

    return data


def get_board_data(board_id):

    client = TrelloClient(**settings.CREDENTIALS)

    board = client.get_board(board_id)
    cards = board.get_cards()

    data = {
        'id': board_id,
        'name': board.name,
        'cards': []
    }

    for card in cards:
        data['cards'].append(get_card_data(card))

    if cards:
        data['todo'] = sum([card['todo'] for card in data['cards']])
        data['done'] = sum([card['done'] for card in data['cards']])
    else:
        data['todo'] = 0
        data['done'] = 0

    return data


def save_current_state():

    boards_processed = 0

    for board_id in settings.BOARDS_TO_FOLLOW:
        board_data = get_board_data(board_id)

        directory = os.path.join(settings.HISTORY_PATH, board_id)
        common.ensure_directory(directory)
        filepath = os.path.join(directory, common.get_today_string())
        common.save_data(board_data, filepath)

        boards_processed += 1

    return boards_processed

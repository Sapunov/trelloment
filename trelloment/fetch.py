"""Trelloment fetcher.
"""

import os

from trello import TrelloClient

from trelloment import settings
from trelloment import common


def get_card_data(card):

    data = {}

    data['name'] = card.name
    data['todo_list'] = []

    card.fetch_checklists()

    if card.checklists:
        for todo in card.checklists[0].items:
            data['todo_list'].append(
                {
                    'name': todo['name'],
                    'is_completed': todo['checked']
                }
            )

        data['todo'] = len(data['todo_list'])
        data['done'] = sum(1 for todo in data['todo_list'] if todo['is_completed'])
    else:
        # When card have no checklist than card have only one task - to complete itself
        # i.e. only one todo.
        # In this case only list where card locats matter(`done` or another)
        data['todo'] = 1
        data['done'] = 1 if card.get_list().name.lower() == 'done' else 0

    data['is_completed'] = True if data['todo'] == data['done'] else False

    return data


def get_board_data(board_id):

    client = TrelloClient(**settings.CREDENTIALS)

    data = {}
    board = client.get_board(board_id)
    cards = board.get_cards()

    data['name'] = board.name
    data['cards'] = []

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

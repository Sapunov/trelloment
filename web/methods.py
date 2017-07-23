from flask.json import jsonify

from trelloment import entities
from trelloment import common


DATETIME_FORMAT = '%Y-%m-%d'


def get_boards_list():

    boards = entities.get_boards()
    ans = []

    for board in boards:
        ans.append({
            'id': board.id,
            'name': board.name,
            'todo': board.todo,
            'done': board.done,
            'is_completed': board.is_completed,
        })

        # todo and done is a methods that count len of the specific lists
        ans[-1]['percent'] = common.percent(ans[-1]['done'], ans[-1]['todo'])

    return jsonify(ans)


def get_board_data(board_id):

    board = entities.get_board_by_id(board_id)
    ans = {
        'id': board.id,
        'name': board.name,
        'todo': board.todo,
        'done': board.done,
        'is_completed': board.is_completed
    }

    ans['percent'] = common.percent(ans['done'], ans['todo'])

    return jsonify(ans)


def get_board_cards(board_id):

    cards = entities.get_board_by_id(board_id).cards
    ans = []

    for card in cards:
        ans.append({
            'id': card.id,
            'name': card.name,
            'todo': card.todo,
            'done': card.done,
            'is_completed': card.is_completed
        })

        ans[-1]['percent'] = common.percent(ans[-1]['done'], ans[-1]['todo'])

    return jsonify(ans)

def get_board_progress(board_id):

    board = entities.get_board_by_id(board_id)
    progress = board.progress(DATETIME_FORMAT)

    return jsonify(progress)


def get_board_diff(board_id):

    board = entities.get_board_by_id(board_id)
    diff = board.diff(DATETIME_FORMAT)

    return jsonify(diff)


def get_card_data(card_id):

    card = entities.get_card_by_id(card_id)
    ans = {
        'id': card.id,
        'name': card.name,
        'todo': card.todo,
        'done': card.done,
        'is_completed':card.is_completed
    }

    ans['percent'] = common.percent(ans['done'], ans['todo'])

    return jsonify(ans)


def get_card_progress(card_id):

    card = entities.get_card_by_id(card_id)
    progress = card.progress(DATETIME_FORMAT)

    return jsonify(progress)


def get_card_diff(card_id):

    card = entities.get_card_by_id(card_id)
    diff = card.diff(DATETIME_FORMAT)

    return jsonify(diff)
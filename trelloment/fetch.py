"""Trelloment fetcher.
"""

from trello import TrelloClient

from trelloment import common
from trelloment import core
from trelloment import settings
from trelloment import structures


log = core.setup_log(__name__)


def get_card(trello_card, board_id):

    trello_card_checklists = trello_card.fetch_checklists()

    card_obj = structures.Card(trello_card.id, load=False)
    card_obj.set_name(trello_card.name)
    card_obj.board_id = board_id

    if trello_card_checklists:
        for task in trello_card_checklists[0].items:
            card_obj.add_task(task['id'], task['name'], task['checked'])

        card_obj.is_completed = True if card_obj.todo == card_obj.done else False
    else:
        # When card have no checklist than card have only
        # one task - to complete itself i.e. only one todo.
        #
        # In this case only list where card locates matter(`done` or another)
        if common.lower_eq(trello_card.get_list().name, settings.DONE_LIST):
            card_obj.is_completed = True

    return card_obj


def get_board(board_id):

    client = TrelloClient(**settings.CREDENTIALS)

    # Load data from Trello.com
    trello_board = client.get_board(board_id)
    trello_cards = trello_board.get_cards()

    # Trelloment object
    board_obj = structures.Board(board_id, load=False)
    board_obj.set_name(trello_board.name)

    for card in trello_cards:
        board_obj.add_card(get_card(card, board_id))

    if board_obj.todo > 0 and board_obj.todo == board_obj.done:
        board_obj.is_completed = True

    return board_obj


def save_current_state():

    log.debug('Start saving current boards state')

    boards_processed = 0

    for board_id in settings.BOARDS_TO_FOLLOW:
        log.debug('Start processing board<%s>', board_id)

        board = get_board(board_id)

        board.save_recursively()

        log.debug('%s saved', board)

        boards_processed += 1

    log.debug('%s boards was processed', boards_processed)

    return boards_processed

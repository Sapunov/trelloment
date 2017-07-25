'''Trelloment web api server
'''

from flask import Flask
from flask import render_template

import methods


app = Flask(__name__)


@app.route('/api/boards')
@app.route('/api/boards/<string:board_id>')
@app.route('/api/boards/<string:board_id>/<string:path>')
def get_board_path(board_id=None, path=None):

    if board_id is None:
        return methods.get_boards_list()

    if path == 'cards':
        return methods.get_board_cards(board_id)
    elif path == 'progress':
        return methods.get_board_progress(board_id)
    elif path == 'diff':
        return methods.get_board_diff(board_id)
    else:
        return methods.get_board_data(board_id)


@app.route('/api/cards/<string:card_id>')
@app.route('/api/cards/<string:card_id>/<string:path>')
def get_card(card_id, path=None):

    if path == 'tasks':
        return methods.get_card_tasks(card_id)
    elif path == 'progress':
        return methods.get_card_progress(card_id)
    elif path == 'diff':
        return methods.get_card_diff(card_id)
    else:
        return methods.get_card_data(card_id)


@app.route('/')
@app.route('/<path:path>')
def index(path=None):

    return render_template('index.html')


def main():

    app.run(debug=True)


if __name__ == '__main__':

    main()

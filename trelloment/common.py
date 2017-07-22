"""Trelloment common functions.
"""

import json
import datetime
import os
import errno
import string


def save_data(data, filename):

    with open(filename, 'w') as opened_file:
        json.dump(data, opened_file)


def load_data(filename):

    with open(filename) as opened_file:
        return json.load(opened_file)


def get_today_string():

    today = datetime.datetime.today()

    return today.strftime('%Y-%M-%d')


def ensure_directory(path):

    try:
        os.makedirs(path)
    except OSError as error:
        if error.errno != errno.EEXIST:
            raise

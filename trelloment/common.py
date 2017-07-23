"""Trelloment common functions.
"""

import pickle
import datetime
import os
import errno
import zlib


def save_data(data, filename):

    with open(filename, 'wb') as opened_file:
        opened_file.write(zlib.compress(pickle.dumps(data)))


def load_data(filename):

    with open(filename, 'rb') as opened_file:

        return pickle.loads(zlib.decompress(opened_file.read()))


def get_today_string():

    today = datetime.datetime.today()

    return today.strftime('%Y-%m-%d')


def ensure_directory(path):

    try:
        os.makedirs(path)
    except OSError as error:
        if error.errno != errno.EEXIST:
            raise


def compress_json(data):

    return zlib.compress(bytes(data, 'utf-8'))


def lower_eq(lhs, rhs):

    return lhs.lower() == rhs.lower()

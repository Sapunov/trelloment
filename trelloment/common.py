"""Trelloment common functions.
"""

import datetime
import errno
import os
import pickle
import zlib

from trelloment import core
from trelloment import settings


log = core.setup_log(__name__)


def save_data(data, filename):

    try:
        with open(filename, 'wb') as opened_file:
            opened_file.write(zlib.compress(pickle.dumps(data)))
    except OSError as error:
        log.exception(error)
        raise


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


def percent(numerator, denominator):

    if denominator == 0:
        return 0.0

    return round(numerator / denominator * 100, 4)

def version2dt(version_str):

    year, month, day = map(int, version_str.split('-'))

    return datetime.datetime(year, month, day)


def dt2fmt(dt, format):

    return dt.strftime(format)

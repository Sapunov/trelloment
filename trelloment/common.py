"""Trelloment common functions.
"""

import datetime
import errno
import os
import pickle
import zlib
import functools

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


def gcd_(a, b):
    '''Greatest common divisor for 2 digits.
    '''

    while b:
        a, b = b, a % b

    return a


def gcd(*items):
    '''Greatest common divisor for the list of digits.
    '''

    if len(items) == 1 and isinstance(items[0], (list, tuple)):
        items = items[0]

    return functools.reduce(gcd_, items)


def lcm(*items):
    '''Least common multiple for the list of digits.
    '''

    if len(items) == 1 and isinstance(items[0], (list, tuple)):
        items = items[0]

    # delete all zeros
    items = [i for i in items if i != 0]

    def compute(lhs, rhs):

        try:
            return (lhs * rhs) // gcd(lhs, rhs)
        except ZeroDivisionError:
            return 0

    return functools.reduce(compute, items, 1)


def safe_divide_dv(digit, vector):

    vector = vector.copy()

    for i in range(len(vector)):
        try:
            vector[i] = int(digit / vector[i])
        except ZeroDivisionError:
            vector[i] = 0

    return vector


def multiple_v(lhs, rhs):

    assert len(lhs) == len(rhs), 'Length must be equal'

    return [lhs[i] * rhs[i] for i in range(len(lhs))]

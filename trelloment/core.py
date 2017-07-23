"""Trelloment core functions.
"""

import logging
import logging.handlers
import os

from trelloment import settings


def setup_log(
        name,
        log_level=logging.DEBUG,
        logs_directory=settings.LOGS_DIR,
        log_file=None
):

    log_format = "%(asctime)s.%(msecs)03d "
    log_format += "(%(filename)15.15s:%(lineno)04d) "
    log_format += "%(levelname)s: %(message)s"

    date_format = "%d.%m.%y %H:%M:%S"

    if log_file is None:
        log_file = os.path.join(logs_directory, settings.NAME + ".log")
    else:
        log_file = os.path.join(logs_directory, os.path.split(log_file)[1])

    log = logging.getLogger(name)
    log.setLevel(log_level)

    base_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=(20 * 1024 ** 2), backupCount=3)
    base_handler.setLevel(log_level)

    base_handler.setFormatter(logging.Formatter(log_format, date_format))

    log.addHandler(base_handler)

    return log

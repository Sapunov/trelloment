"""Trelloment cron task for save current state of boards
"""

from trelloment import fetch
from trelloment import core


log = core.setup_log(__name__, log_file='save_current_state')


def main():

    try:
        fetch.save_current_state()
    except Exception as error:
        log.exception(error)


if __name__ == '__main__':

    main()

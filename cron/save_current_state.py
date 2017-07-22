"""Trelloment cron task for save current state of boards
"""

from trelloment import fetch


def main():

    boards_processed = fetch.save_current_state()

    print('{0} boards was processed'.format(boards_processed))


if __name__ == '__main__':

    main()

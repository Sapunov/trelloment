"""Trelloment datastructures.
"""

import os

from trelloment import settings
from trelloment import common
from trelloment import exceptions


class Base:
    '''Base datastructure for Card and Board.
    '''

    def __init__(self):

        self.id = None
        self.name = None
        self.version = None

        self._loaded = False

    def load(self):

        raise NotImplementedError

    def save(self):

        raise NotImplementedError

    def get_entity_dir(self):
        '''Get entity(Card or Board) directory path.

        Create specific directory if that doesn't exist.
        '''

        if self.__class__.__name__ == 'Card':
            entity_type = 'card'
        elif self.__class__.__name__ == 'Board':
            entity_type = 'board'
        else:
            entity_type = ''

        directory = os.path.join(settings.HISTORY_PATH, entity_type, self.id)
        common.ensure_directory(directory)

        return directory

    def get_today_path(self):

        return os.path.join(self.get_entity_dir(), common.get_today_string())

    def load_version_data(self, version):

        return common.load_data(os.path.join(self.get_entity_dir(), version))

    def get_last_version(self):

        try:
            return self.versions[-1]
        except IndexError:
            raise exceptions.NoVersionAvailible

    def set_name(self, entity_name):
        '''Name is a load indicator.
        '''

        self.name = entity_name
        self._loaded = True


    def try_to_load(self):

        try:
            self.load()
        except (FileNotFoundError, exceptions.NoVersionAvailible):
            pass

    def progress(self, dtformat=None):

        points = []

        for version in self.versions:
            self.load(version)

            points.append((
                common.dt2fmt(common.version2dt(version), dtformat) \
                    if dtformat else common.version2dt(version),
                self.todo,
                self.done,
                common.percent(self.done, self.todo)
            ))

        # The last item in self.versions is the lastest version
        # i.e current version will be the last one

        return points

    def _diff(self, todos, dones, i):

        l = dones[i - 1] / todos[i - 1]
        r = dones[i] / todos[i]

        return round((r - l) * 100, 4)

    def diff(self, dtformat=None):

        points = []
        versions = self.versions
        todos = []
        dones = []

        for version in versions:
            self.load(version)
            todos.append(self.todo)
            dones.append(self.done)

        for i in range(1, len(versions)):
            points.append((
                common.dt2fmt(common.version2dt(versions[i]), dtformat) \
                    if dtformat else common.version2dt(versions[i]),
                self._diff(todos, dones, i)
            ))

        return points

    @property
    def versions(self):

        return sorted(os.listdir(self.get_entity_dir()))

    def __str__(self):

        entity_name = self.__class__.__name__

        return '<{0}: {1} - {2}>'.format(entity_name, self.id, self.name)

    def __repr__(self):

        return self.__str__()


class Task:
    '''Task datastructure.

    !!! WARNING: this datastructure is IMMUTABLE because we save it as it is
                 using pickle for serialization!
    '''

    def __init__(self, task_id, task_name, is_task_completed):

        self.id = task_id
        self.name = task_name
        self.is_completed = is_task_completed

    def __str__(self):

        return '<Task: {0} - {1}>'.format(self.id, self.name)

    def __repr__(self):

        return self.__str__()


class Card(Base):
    '''Card datastructure.
    '''

    def __init__(self, card_id, load=True):

        super().__init__()

        self.id = card_id
        self.tasks = []
        self.is_completed = False
        self.board_id = None

        if load:
            self.try_to_load()

    @property
    def todo(self):
        '''How many tasks to do.
        '''

        return len(self.tasks)

    @property
    def done(self):
        '''How many tasks already done.
        '''

        return sum(1 for task in self.tasks if task.is_completed)

    def add_task(self, task_id, task_name, is_task_completed):

        self.tasks.append(Task(task_id, task_name, is_task_completed))

    def save(self):

        data = {
            'board_id': self.board_id,
            'name': self.name,
            'is_completed': self.is_completed,
            'tasks': self.tasks
        }

        common.save_data(data, self.get_today_path())

    def load(self, version=False):

        version = version or self.get_last_version()

        data = self.load_version_data(version)

        self.board_id = data['board_id']
        self.is_completed = data['is_completed']
        self.tasks = data['tasks']
        self.version = version
        self.set_name(data['name'])


class Board(Base):
    '''Board datastructure.
    '''

    def __init__(self, board_id, load=True):

        super().__init__()

        self.id = board_id
        self.cards = []
        self.is_completed = False

        if load:
            self.try_to_load()

    @property
    def todo(self):
        '''How many tasks to do.
        '''

        return len(self.cards)

    @property
    def done(self):
        '''How many tasks already done.
        '''

        return sum(1 for card in self.cards if card.is_completed)

    def add_card(self, card_obj):

        self.cards.append(card_obj)


    def save(self):

        data = {
            'name': self.name,
            'is_completed': self.is_completed,
            'cards_ids': [card.id for card in self.cards]
        }

        common.save_data(data, self.get_today_path())


    def save_recursively(self):

        for card in self.cards:
            card.save()

        self.save()

    def load(self, version=False):

        version = version or self.get_last_version()

        data = self.load_version_data(version)

        self.is_completed = data['is_completed']

        self.cards = []

        for card_id in data['cards_ids']:
            # Load card with the same version
            card = Card(card_id, load=False)
            card.load(version)

            self.cards.append(card)

        self.version = version
        self.set_name(data['name'])

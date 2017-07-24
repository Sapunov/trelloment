"""Trelloment installation script."""

from __future__ import unicode_literals
from setuptools import find_packages, setup


if __name__ == '__main__':
    with open('README.md') as readme:
        setup(
            name='trelloment',
            version='1.0',

            description=readme.readline().strip(),
            long_description=readme.read().strip() or None,
            url='https://github.com/sapunov/trelloment',

            license='GPL3',
            author='Nikita Sapunov',
            author_email='kiton1994@gmail.com',

            classifiers=[
                'Intended Audience :: Everybody',
                'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                'Operating System :: MacOS :: MacOS X',
                'Operating System :: POSIX',
                'Operating System :: Unix',
                'Programming Language :: Python :: 3'
            ],
            platforms=['unix', 'linux', 'osx', 'windows'],

            install_requires=['requests', 'py-trello'],
            packages=find_packages(),
        )

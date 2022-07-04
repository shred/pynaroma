#
# pynaroma - tools for converting Amiga ROMs and binaries
#
# Copyright (C) 2021 Richard "Shred" Körber
#   https://github.com/shred/pynaroma
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='pynaroma',
    version='0.4.0',
    description='Tools for converting Amiga ROM images',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/shred/pynaroma',
    keywords='Amiga ROM',
    license='GPLv3+',

    python_requires='>=3',

    author='Richard Körber',
    author_email='dev@shredzone.de',

    project_urls={
        'Source': 'https://github.com/shred/pynaroma',
        'Tracker': 'https://github.com/shred/pynaroma/issues',
    },

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Build Tools',
        'Topic :: System :: Emulators',
        'Topic :: System :: Hardware',
        'Topic :: System :: Operating System',
        'Topic :: System :: Software Distribution',
        'Topic :: Utilities'
    ],

    packages=['pynaroma'],

    entry_points={
        'console_scripts': [
            'rom2bin=pynaroma.rom2bin:main',
            'bin2rom=pynaroma.bin2rom:main',
            'bin2split=pynaroma.bin2split:main',
        ],
    },
)

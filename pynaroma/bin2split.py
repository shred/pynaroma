#!/usr/bin/env python3
#
# pynaroma - tools for converting Amiga ROMs and binaries
#
# Copyright (C) 2022 Richard "Shred" Körber
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

import argparse
import re
import sys

class SizeAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        m = re.match(r'^(\d+)([KMG]?)i?B?$', values)
        if m is None:
            parser.error('{} must be a number with optional IEC unit prefix (e.g. "64K")'.format(self.dest))
            return
        value = int(m.group(1))
        prefix = m.group(2)
        if prefix == 'K':
            value *= 1024
        elif prefix == 'M':
            value *= 1024*1024
        elif prefix == 'G':
            value *= 1024*1024*1024
        if value < 8192:
            parser.error('{}: {} bytes is quite small! Did you forget to give an IEC unit prefix?'.format(self.dest, value))
            return
        setattr(namespace, self.dest, value)

def appendIndex(fileName, index):
    m = re.compile(r'^(.*)(\.[^.]+)$').match(fileName)
    if m:
        return '%s-%d%s' % (m.group(1), index, m.group(2))
    return '%s-%d' % (fileName, index)

def splitFile(fileName, size):
    with open(fileName, 'rb') as source:
        data = source.read(1)
        for ix in range(128):
            limit = size
            if len(data) > 0:
                with open(appendIndex(fileName, ix), 'wb') as target:
                    while limit > 0 and len(data) > 0:
                        limit -= 1
                        target.write(bytes([data[0]]))
                        data = source.read(1)
        if len(data) > 0:
            print('Generated more than 128 fragments. This cannot be right. Please check your size option!', file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description='Convert ROM dumps to BIN images')
    parser.add_argument('file',
                nargs=1,
                metavar='BIN',
                help='BIN image file name to be split. Index number will be attached to file name if split option is used.')
    parser.add_argument('-s', '--size',
                dest='size',
                required=True,
                action=SizeAction,
                help='Size of the target files, in bytes. IEC unit prefix is accepted (e.g. "64K").')
    args = parser.parse_args()

    splitFile(args.file[0], args.size)

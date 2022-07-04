#!/usr/bin/env python3
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

import argparse
import sys

def write32bit(lowFile, highFile, sourceFiles, duplicate=False, littleendian=False):
    with lowFile as low:
        with highFile as high:
            for srcFile in sourceFiles:
                with open(srcFile, 'rb') as src:
                    while data := src.read(4):
                        low.write(bytes([
                            data[0 if littleendian else 3],
                            data[1 if littleendian else 2]
                        ]))
                        high.write(bytes([
                            data[2 if littleendian else 1],
                            data[3 if littleendian else 0]
                        ]))
                if duplicate:
                    with open(srcFile, 'rb') as src:
                        while data := src.read(4):
                            low.write(bytes([
                                data[0 if littleendian else 3],
                                data[1 if littleendian else 2]
                            ]))
                            high.write(bytes([
                                data[2 if littleendian else 1],
                                data[3 if littleendian else 0]
                            ]))

def write16bit(targetFile, sourceFiles, duplicate=False, littleendian=False):
    with targetFile as target:
        for srcFile in sourceFiles:
            with open(srcFile, 'rb') as src:
                while data := src.read(2):
                    target.write(bytes([
                        data[0 if littleendian else 1],
                        data[1 if littleendian else 0]
                    ]))
            if duplicate:
                with open(srcFile, 'rb') as src:
                    while data := src.read(2):
                        target.write(bytes([
                            data[0 if littleendian else 1],
                            data[1 if littleendian else 0]
                        ]))

def write8bit(lowFile, highFile, sourceFiles, duplicate=False, littleendian=False):
    with lowFile as low:
        with highFile as high:
            for srcFile in sourceFiles:
                with open(srcFile, 'rb') as src:
                    while data := src.read(2):
                        low.write(bytes([data[0 if littleendian else 1]]))
                        high.write(bytes([data[1 if littleendian else 0]]))
                if duplicate:
                    with open(srcFile, 'rb') as src:
                        while data := src.read(2):
                            low.write(bytes([data[0 if littleendian else 1]]))
                            high.write(bytes([data[1 if littleendian else 0]]))


def main():
    parser = argparse.ArgumentParser(description='Convert ROM dumps to BIN images')
    parser.add_argument('files',
                nargs='+',
                metavar='ROM',
                help='Source ROM files. Multiple files will be concatenated.')
    parser.add_argument('-o', '--to',
                metavar='BIN',
                type=argparse.FileType('wb'),
                help='Target BIN image file name for a single 16-bit file.')
    parser.add_argument('-L', '--low',
                metavar='BIN-LOW',
                type=argparse.FileType('wb'),
                help='Target BIN image file name for the lower 32-bit file.')
    parser.add_argument('-H', '--high',
                metavar='BIN-HIGH',
                type=argparse.FileType('wb'),
                help='Target BIN image file name for the higher 32-bit file.')
    parser.add_argument('-d', '--duplicate',
                dest='duplicate',
                action='store_true',
                help='Writes each source ROM file twice.')
    parser.add_argument('-8', '--8bit',
                dest='bit8',
                action='store_true',
                help='Enable 8 bit mode.')
    parser.add_argument('-l', '--little', '--littleendian',
                dest='littleendian',
                action='store_true',
                help='Uses little-endian mode, default is big-endian.')
    args = parser.parse_args()

    if (args.low and not args.high) or (not args.low and args.high):
        print('--low and --high options must be given together.', file=sys.stderr)
        parser.print_help(sys.stderr)
        exit(1)

    if args.to and (args.low or args.high):
        print('--to cannot be combined with --low and --high.', file=sys.stderr)
        parser.print_help(sys.stderr)
        exit(1)

    if args.bit8 and not (args.low or args.high):
        print('--8bit requires --low and --high options.', file=sys.stderr)
        parser.print_help(sys.stderr)
        exit(1)

    if args.low and args.high:
        if args.bit8:
            write8bit(args.low, args.high, args.files, duplicate=args.duplicate, littleendian=args.littleendian)
        else:
            write32bit(args.low, args.high, args.files, duplicate=args.duplicate, littleendian=args.littleendian)
    else:
        write16bit(args.to, args.files, duplicate=args.duplicate, littleendian=args.littleendian)

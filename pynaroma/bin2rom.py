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
import os
import re
import sys

def appendIndex(fileName, index):
    m = re.compile(r'^(.*)(\.[^.]+)$').match(fileName)
    if m:
        return '%s-%d%s' % (m.group(1), index, m.group(2))
    return '%s-%d' % (fileName, index)

def getFileSize(file):
    return os.path.getsize(file.name)

def read32bit(lowFile, highFile, targetFileName, limit=None, littleendian=False):
    endianHighFile = lowFile if littleendian else highFile
    endianLowFile = highFile if littleendian else lowFile
    with open(targetFileName, 'wb') as target:
        while limit is None or limit > 0:
            if limit is not None:
                limit -= 4
            if not (data := endianHighFile.read(2)):
                break
            target.write(bytes([
                data[0 if littleendian else 1],
                data[1 if littleendian else 0]
            ]))
            if not (data := endianLowFile.read(2)):
                break
            target.write(bytes([
                data[0 if littleendian else 1],
                data[1 if littleendian else 0]
            ]))

def read16bit(sourceFile, targetFileName, limit=None, littleendian=False):
    with open(targetFileName, 'wb') as target:
        while limit is None or limit > 0:
            if limit is not None:
                limit -= 2
            if not (data := sourceFile.read(2)):
                break
            target.write(bytes([
                data[0 if littleendian else 1],
                data[1 if littleendian else 0]
            ]))

def read8bit(lowFile, highFile, targetFileName, limit=None, littleendian=False):
    endianHighFile = lowFile if littleendian else highFile
    endianLowFile = highFile if littleendian else lowFile
    with open(targetFileName, 'wb') as target:
        while limit is None or limit > 0:
            if limit is not None:
                limit -= 2
            if not (data := endianHighFile.read(1)):
                break
            target.write(bytes([data[0]]))
            if not (data := endianLowFile.read(1)):
                break
            target.write(bytes([data[0]]))

def splitRead32bit(lowFile, highFile, baseFileName, split, littleendian=False):
    lowSize = getFileSize(lowFile)
    highSize = getFileSize(highFile)
    if lowSize != highSize:
        print('--low and --high files have different sizes.', file=sys.stderr)
        exit(1)
    fileSize = lowSize + highSize
    if fileSize % split != 0:
        print('Cannot split source file size {} into {} chunks.'.format(fileSize, split), file=sys.stderr)
        exit(1)
    limit = fileSize // split
    for ix in range(split):
        read32bit(lowFile, highFile, appendIndex(baseFileName, ix), limit, littleendian)

def splitRead16bit(sourceFile, baseFileName, split, littleendian=False):
    fileSize = getFileSize(sourceFile)
    if fileSize % split != 0:
        print('Cannot split source file size {} into {} chunks.'.format(fileSize, split), file=sys.stderr)
        exit(1)
    limit = fileSize // split
    for ix in range(split):
        read16bit(sourceFile, appendIndex(baseFileName, ix), limit, littleendian)

def splitRead8bit(sourceFile, baseFileName, split, littleendian=False):
    fileSize = getFileSize(sourceFile)
    if fileSize % split != 0:
        print('Cannot split source file size {} into {} chunks.'.format(fileSize, split), file=sys.stderr)
        exit(1)
    limit = fileSize // split
    for ix in range(split):
        read8bit(sourceFile, appendIndex(baseFileName, ix), limit, littleendian)

def main():
    parser = argparse.ArgumentParser(description='Convert BIN images to ROM dumps')
    parser.add_argument('file',
                nargs=1,
                metavar='ROM',
                help='Target ROM file name. Index number will be attached to file name if split option is used.')
    parser.add_argument('-f', '--from',
                metavar='BIN',
                dest='source',
                type=argparse.FileType('rb'),
                help='Source BIN image file name for a single 16-bit file.')
    parser.add_argument('-L', '--low',
                metavar='BIN-LOW',
                type=argparse.FileType('rb'),
                help='Source BIN image file name for the lower 32-bit file.')
    parser.add_argument('-H', '--high',
                metavar='BIN-HIGH',
                type=argparse.FileType('rb'),
                help='Source BIN image file name for the higher 32-bit file.')
    parser.add_argument('-s', '--split',
                dest='split',
                type=int,
                choices=[1,2,4,8],
                help='Split image into this number of ROM files.')
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

    if args.source and (args.low or args.high):
        print('--from cannot be combined with --low and --high.', file=sys.stderr)
        parser.print_help(sys.stderr)
        exit(1)

    if args.bit8 and not (args.low or args.high):
        print('--8bit requires --low and --high options.', file=sys.stderr)
        parser.print_help(sys.stderr)
        exit(1)

    if args.split is not None:
        bad = False
        if not (args.low is None or args.low.seekable()):
            print('--low file must be seekable.', file=sys.stderr)
            bad |= True
        if not (args.high is None or args.high.seekable()):
            print('--high file must be seekable.', file=sys.stderr)
            bad |= True
        if not (args.source is None or args.source.seekable()):
            print('--from file must be seekable.', file=sys.stderr)
            bad |= True
        if bad:
            parser.print_help(sys.stderr)
            exit(1)

    if args.low and args.high:
        if args.bit8:
            if args.split is not None and args.split != 1:
                splitRead8bit(args.low, args.high, args.file[0], args.split, littleendian=args.littleendian)
            else:
                read8bit(args.low, args.high, args.file[0], littleendian=args.littleendian)
        else:
            if args.split is not None and args.split != 1:
                splitRead32bit(args.low, args.high, args.file[0], args.split, littleendian=args.littleendian)
            else:
                read32bit(args.low, args.high, args.file[0], littleendian=args.littleendian)
    else:
        if args.split is not None and args.split != 1:
            splitRead16bit(args.source, args.file[0], args.split, littleendian=args.littleendian)
        else:
            read16bit(args.source, args.file[0], littleendian=args.littleendian)

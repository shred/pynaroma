# pynaroma

This is a tiny collection of command line tools for generating Amiga ROM files from ROM dumps, and vice versa. It takes care for byte swapping, splitting, and merging different ROM files.

## Installation

_pynaroma_ is written in Python 3.

```sh
pip install pynaroma
```

## Terminology

In the following examples two kinds of files are mentioned. Both have different purposes, so do not mix them up.

`*.rom` files are ROM dumps that are generated by tools like [GrabKick](http://aminet.net/package/util/misc/GrabKick) and can be directly used in [Amiga emulators](https://fs-uae.net/). Bytes are in correct order, so strings are correct if you read the dump file with a Hex editor.

`*.bin` files are ROM images that are suitable to be burned into EPROMs. There may be two separate ROM image files for the lower and higher ROM in 32-bit Amigas. Also bytes are swapped, so these files can be read by programmer tools like [minipro](https://gitlab.com/DavidGriffith/minipro).

## Tools

* `rom2bin` - Converts ROM dumps into one or two ROM image files, ready for burning.
* `bin2rom` - Converts one or two ROM image files into one or multiple ROM dumps.

## Examples

These are some common usage examples of the tool. Both tools are meant to be used by experienced users, so they are not too smart and will generate broken output if you give a broken input.

----

Convert an AmigaOS 3.2 ROM dump for the Amiga 500 into a single EPROM image fit for burning:

```sh
rom2bin --to kick32.bin kickcdtva1000a500a2000a600.rom
```

Both the source and the target files are 512KB large.

----

Convert an AmigaOS 3.2 ROM dump for the Amiga 4000 into two EPROM images for burning into high and low ROMs:

```sh
rom2bin --low kick32-low.bin --high kick32-high.bin kicka4000.rom
```

The source file is 512KB large, and is split into two target files of 256KB each.

----

If 512KB EPROMs are used, the ROM image must be duplicated to fill the entire memory. The `--duplicate` option will duplicate each of the given ROM dumps.

```sh
rom2bin --low kick32-low.bin --high kick32-high.bin --duplicate kicka4000.rom
```

Now both target files are 512KB each, and will fit into the 512KB EPROM.

----

If an adapter board with a bigger EPROM and a switch is used, it is also possible to burn different ROM images, e.g. to switch between two different AmigaOS versions:

```sh
rom2bin --to amiga500.bin kick2-04.rom kick3-2.rom
```

If both `.rom` dumps are 512KB each, the resulting image fits into an 1MB EPROM.

----

If the ROM dumps have different sizes, they can be given as parameter multiple times. In the following example, `kick1-3.rom` is 256KB and `kick2-04.rom` is 512KB large. To create an 1MB ROM dump, `kick1-3.rom` must be duplicated, but `kick2-04.rom` must not. For this reason, the `--duplicate` option cannot be used, but the dump must be given multiple times:

```sh
rom2bin --to amiga500.bin kick1-3.rom kick1-3.rom kick2-04.rom
```

The resulting `.bin` file is 1MB large, and permits to switch between Kick 1.3 and Kick 2.04.

----

`bin2rom` works in the opposite direction. It takes ROM images (that are read from Amiga ROMs or EPROMs), and converts them to ROM dumps that can be stored or used in emulators.

This example joins an Amiga 500 ROM image into a ROM dump. It's the counterpart to the first example above.

```sh
bin2rom --from kick32.bin kickcdtva1000a500a2000a600.rom
```

----

To join the dumps of _high_ and _low_ ROM files, they need to be stated separately:

```sh
bin2rom --low kick32-low.bin --high kick32-high.bin amiga4000.rom
```

As mentioned in the example above, the `kick32-low.bin` and `kick32-high.bin` contain the Kickstart twice, to fill the entire EPROM space. For this reason, the resulting `amiga4000.rom` file is 1MB large and also contains the ROM content twice.

----

You can use the `--split` option to split a ROM image into a number of equally-sized dumps:

```sh
bin2rom --split 2 --low kick32-low.bin --high kick32-high.bin amiga4000.rom
```

The resulting files will be called `amiga4000-1.rom` and `amiga4000-2.rom`. Each file contains the first or second half of the ROM image, respectively.

`--split 4` would split the image into four ROM dump files, `--split 8` would split the image into eight ROM dumps. Other values (like `--split 3`) are not allowed because they would make no sense for obvious reasons.

## Contribute

* Fork the [Source code at GitHub](https://github.com/shred/pynaroma). Feel free to send pull requests.
* Found a bug? [File a bug report!](https://github.com/shred/pynaroma/issues)

## License

_pynaroma_ is open source software. The source code is distributed under the terms of [GNU General Public License (GPLv3)](https://www.gnu.org/licenses/gpl-3.0.en.html#content).

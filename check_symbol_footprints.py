#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Why even is this script?

This script takes a bunch of symbol libraries (.lib files),
and a whole heap of footprint libraries (.pretty directories),
and determines which symbols need their footprint associations updated.

Tests tested:

a) Symbol is missing a footprint (this is OK, some are generic)
b) Symbol footprint pattern is illegal (should be of the form <FpLib:FpName>)
c) Referenced footprint library or footprint name is missing

How to use?

python check_symbol_footprints.py -h

"""

from __future__ import print_function

import argparse
import sys
import os
import os.path

sys.path.append("schlib")

import schlib

parser = argparse.ArgumentParser(description="Check symbol footprint associations")
parser.add_argument("symbols", help="Path to symbol libraries (.lib files) to check")
parser.add_argument("footprints", help="Path to footprint libraries (.pretty dirs) to check")
parser.add_argument("-a", "--all", help="Show all errors", action="store_true")
parser.add_argument("-e", "--empty", help="Show symbols with empty footprints", action="store_true")
parser.add_argument("-p", "--pattern", help="Show symbols with incorrect footprint pattern (LibName:FpName)", action="store_true")
parser.add_argument("-n", "--name", help="Show symbols that point to an incorrect footprint", action="store_true")

args = parser.parse_args()

symbols_dir = args.symbols
footprints_dir = args.footprints

symbols = [f for f in os.listdir(symbols_dir) if f.endswith('.lib')]
footprints = [f for f in os.listdir(footprints_dir) if f.endswith('.pretty')]

"""
Various classes of errors:

- Footprint field is empty (no associated footprint)
- Footprint field does not match Nickname:Fpname pattern
- Footprint library 'nickname' does not exist
- Footprint name 'Fpname' does not exist

Each error type is stored in a dict, based on the library name
Each error instance stores [symbol_name, footprint_text]

"""

err_fp_empty = {}
err_fp_pattern = {}
err_fp_nickname = {}
err_fp_fpname = {}

def addError(lib_name, sym_name, fp_text, err_dict):
    if not lib_name in err_dict:
        err_dict[lib_name] = []

    err_dict[lib_name].append([sym_name, fp_text])


def printError(err_dict):
    for lib in err_dict:
        print("-" * (9 + len(lib)))
        print("Library:", lib)
        for cmp in err_dict[lib]:
            print(cmp[0], "->", cmp[1])


# Construct a dictionary of Nickname:FpName
# Remove the .pretty suffix from each directory
# Remove the .kicad_mod suffix from each footprint
fp_lib_list = {}

for fp_lib in footprints:

    pretty = os.path.join(footprints_dir, fp_lib)

    if not pretty.endswith(".pretty") or not os.path.isdir(pretty):
        continue

    footprints = [f.replace('.kicad_mod', '') for f in os.listdir(pretty) if f.endswith('.kicad_mod')]
    nickname = fp_lib.split(os.path.sep)[-1].replace('.pretty', '')
    fp_lib_list[nickname] = footprints

print("Checking libraries...\n")

for sym_lib in symbols:
    library = os.path.join(symbols_dir, sym_lib)

    sch = schlib.SchLib(library)

    for c in sch.components:
        # Extract footprint and name information
        cmp_name = c.name

        # Empty footprint?
        if not c.hasFootprint():
            addError(sym_lib, cmp_name, '', err_fp_empty)
            continue

        fp = c.getFootprint()

        fp_split = fp.split(":")

        correct_pattern = len(fp_split) == 2 and len(fp_split[0]) > 0 and len(fp_split[1]) > 0

        if not correct_pattern:
            addError(sym_lib, cmp_name, fp, err_fp_pattern)
            continue

        fp_nickname, fp_name = fp_split

        # Test that the footprint library (nickname) exists
        if not fp_nickname in fp_lib_list:
            addError(sym_lib, cmp_name, fp, err_fp_nickname)
            continue

        # Test that the footprint exists
        fp_list = fp_lib_list[fp_nickname]

        if not fp_name in fp_list:
            addError(sym_lib, cmp_name, fp, err_fp_fpname)
            continue

# Print out the errors!

if args.empty or args.all:
    if len(err_fp_empty) > 0:
        print("Symbols with empty footprint field:")
        printError(err_fp_empty)

if args.pattern or args.all:
    if len(err_fp_pattern) > 0:
        print("Symbols with incorrect footprint pattern:")
        printError(err_fp_pattern)

if args.name or args.all:
    if len(err_fp_nickname) > 0:
        print("Symbols pointing to missing fp library:")
        printError(err_fp_nickname)
    if len(err_fp_fpname) > 0:
        print("Symbols pointing to missing footprint:")
        printError(err_fp_fpname)
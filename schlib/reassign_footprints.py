#!/usr/bin/env python

"""
This script reassigns footprint libraries to .lib symbol files

e.g. when a footprint library is renamed, footprint association
changes from

OldLibrary:FPName

to

NewLibrary:FPName

- Reassignment can be done via JSON file
- Reassignment can be performed interactively
"""

from __future__ import print_function

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import argparse
import json
import re
from glob import glob
import os

parser = argparse.ArgumentParser(description="Reassociate footprints after library names are altered")
parser.add_argument('-l', '--libs', action='store', help='Symbol libraries (.lib files)', nargs='+')
parser.add_argument('-p', '--pretty', action='store', help='Footprint libraries (.pretty dirs)', nargs='+')
parser.add_argument('-j', '--json', action='store', help='JSON remapping file')
parser.add_argument('-i', '--interactive', action='store_true', help='Run interactive mode')
parser.add_argument('-r', '--real', action='store', help='Run output (dry-run unless specified)')
parser.add_argument('-f', '--force', action='store', help='Force override even if current association is OK')
parser.add_argument('-v', '--verbose', action='count', help='Print extra debugging information')

args = parser.parse_args()

if not args.verbose:
    args.verbose = 0

libfiles = []
valid_fp_libs = set()

if not args.libs:
    print("No lib files specified")
    sys.exit(1)

for l in args.libs:
    if not os.path.exists(l):
        continue
    if not l.endswith('.lib'):
        continue
    libfiles.append(os.path.abspath(l))

if not args.pretty:
    print("No footprint libraries specified")
    sys.exit(1)

for p in args.pretty:
    if not os.path.exists(p) or not os.path.isdir(p):
        continue
    if not p.endswith('.pretty'):
        continue

    valid_fp_libs.add(os.path.basename(p).replace('.pretty',''))

# Map old libs to new libs

if args.json:
    with open(args.json) as f:
        fp_lib_names = json.loads(f.read())

else:
    fp_lib_names = {}

# Scan through each library file and find erroneous libraries
for l in args.libs:

    if args.verbose:
        print("Reading " + os.path.basename(l))

    output = ""

    with open(l) as f:
        for line in f:

            s = r'^F2 "([^\:]*):(?:[^\:"]*)"'

            result = re.search(s, line)

            new_name = None

            if result and len(result.groups()) > 0:
                fp_lib = result.groups()[0]

                if fp_lib in valid_fp_libs:
                    if args.verbose > 1:
                        print("Valid library -", fp_lib)
                        continue

                else:
                    if fp_lib in fp_lib_names:
                        new_name = fp_lib_names[fp_lib]
                    elif args.interactive:
                        new_name = str(raw_input("Enter new name for '{fp}' (blank to skip)".format(fp=fp_lib)))

                # Add new association to the list
                if new_name and not fp_lib in fp_lib_names:
                    fp_lib_names[fp_lib] = new_name

                    line = line.replace(fp_lib, new_name)

            output += line

    if args.real:
        with open(l, 'w') as op_file:
            op_file.write(output)
                
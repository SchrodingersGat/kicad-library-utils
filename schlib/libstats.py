#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

This file compares two .lib files and generates a list of deleted / added / updated components.
This is to be used to compare an updated library file with a previous version to determine which components have been changed.

"""

from __future__ import print_function
import argparse
import sys
from schlib import *
from print_color import *
import os
from glob import glob

parser = argparse.ArgumentParser( description="Calculate Library Statistics for a given library" )
parser.add_argument( "libfiles", nargs="+", help="List of .lib files to parse" )

args = parser.parse_args()

# Generate list of library files
libfiles = []

for libs in args.libfiles:
    libfiles += glob( libs ) 
    
lib_infos = []

def KLCCheck( lib ):
    call = 'python checklib.py "{lib}" -ss'.format( lib=lib )
    
    return os.system( call )

for libfile in libfiles:

    if not libfile.endswith( ".lib" ) or not os.path.exists( libfile ):
        continue
        
    lib = SchLib( libfile )
    
    n_unique = 0
    n_aliased = 0 
    
    for c in lib.components:
        n_unique += 1
        n_aliased += len( c.aliases )
    
    n_total = n_unique + n_aliased
    
    # KLC errors
    n_errors = KLCCheck( libfile )
    
    # KLC compliance percentage
    if n_total > 0:
        klc_percent = round( float( n_errors ) / n_total * 100, 1 ) 
    else:
        klc_percent = 0
        
    klc_percent = str( klc_percent ) + "%"
    
    # Output stats for this library
    lib_info = []
    
    # Fields
    name = os.path.basename( libfile )
    lib_info.append( "`" + name + "`" )
    lib_info.append( "" ) # Description
    lib_info.append( n_total )
    lib_info.append( klc_percent )
    lib_info.append( "" ) # Notes
    
    line = "| " + " | ".join( map( str, lib_info ) ) + " |"
    print( line )
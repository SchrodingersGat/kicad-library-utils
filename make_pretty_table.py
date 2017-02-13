from __future__ import print_function

import urllib.request as urlrequest
import re
import sys
import time
import os

KLC_DIR = "C:\\kicad\\utils\\pcb"

LIBS_DIR = "C:\\kicad\\share\\pretty"
GITHUB_FP_LIB_TABLE = "https://raw.githubusercontent.com/KiCad/kicad-library/master/template/fp-lib-table.for-github"
GITHUB_BASE = "https://www.github.com/kicad/"

def Fail(msg, result=-1):
    print(msg)
    sys.exit(result)

def CheckFootprint(fp):
    if not os.path.exists(fp):
        return true

    call = 'python "{chk}" "{fp}" -s'.format(
        chk = os.path.sep.join([KLC_DIR,'check_kicad_mod.py']),
        fp = fp)

    #print(call)
    #sys.exit(0)
    return os.system(call) == 0

try:
    # Download the footprint-library-table
    print("Downloading .pretty library table from Github")
    result = urlrequest.urlopen(GITHUB_FP_LIB_TABLE)
    lib_table_data = result.read().decode("utf-8")
except:
    Fail("Error loading fp-lib-table from github.")
    
# Extract .pretty library information
PRETTY_REGEX = 'lib \(name ([^\)]*)\)\(type Github\)\(uri \${KIGITHUB}\/([^\)]*)\)\(options "[^"]*"\)\(descr ([^\)]*)'
    
libs = lib_table_data.split("\n")

good_table = []
deprecated_table = []

def TableHeader():
    header = "| Library | Description | Footprints |\n" # KLC Compliance |\n"
    header += "|---|---|---|\n" #---|\n"

    return header

def TableLine(name,url,description):
    
    pretty = os.path.sep.join([LIBS_DIR, url])
    files = os.listdir(pretty)
    files = [f for f in files if f.endswith(".kicad_mod")]

    n = len(files)

    # KLC compliance
    """
    klc_errors = 0
    for f in files:
        f = os.path.sep.join([LIBS_DIR, url, f])
        if not CheckFootprint(f):
            klc_errors += 1

    
    percent = (n - klc_errors) / n * 100
    """
    line = "| [{name}]({url}) | {description} | {n} |".format(
        name=name,
        url=GITHUB_BASE+url,
        description=description,
        n=n)

    return line
    

# Parse each line of the fp-lib-table file, and extract .pretty library information
for lib in libs:
    result = re.search(PRETTY_REGEX, lib)

    if not result or len(result.groups()) is not 3:
        continue
        
    name, url, description = result.groups()

    description = description.replace('"','')
    
    line = TableLine(name,url,description)
    
    # Ignore libraries marked as 'deprecated'
    if "deprecated" in description.lower():
        deprecated_table.append(line)
    else:
        good_table.append(line)

output = "## Footprint Libraries\n\n"
output += "Footprint libraries are maintained as individual `.pretty` repositories. The tables below list the available footprint libraries."
output += "\n\n"
output += TableHeader()
output += "\n".join(good_table)
output += "\n\n"

output += "## Deprecated Libraries\n\n"
output += "The following libraries are deprecated, and are included only for legacy use. No updates will be accepted for these libraries."
output += "\n\n"
output += TableHeader()
output += "\n".join(deprecated_table)
        
with open("pretty.md","w") as pretty:
    pretty.write(output)

print("Done")

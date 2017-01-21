from __future__ import print_function

import urllib.request as urlrequest
import re
import sys

GITHUB_FP_LIB_TABLE = "https://raw.githubusercontent.com/KiCad/kicad-library/master/template/fp-lib-table.for-github"

def Fail(msg, result=-1):
    print(msg)
    sys.exit(result)

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
    header = "| Library | Description |\n"
    header += "|---|---|\n"

    return header

def TableLine(name,url,description):
    GITHUB_BASE = "https://www.github.com/kicad/"
    line = "| [{name}]({url}) | {description} |".format(name=name,url=GITHUB_BASE+url,description=description)

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
output += TableHeader()
output += "\n".join(good_table)
output += "\n\n"

output += "## Deprecated Libraries\n\n"
output += TableHeader()
output += "\n".join(deprecated_table)
        
with open("pretty.md","w") as pretty:
    pretty.write(output)

print("Done")

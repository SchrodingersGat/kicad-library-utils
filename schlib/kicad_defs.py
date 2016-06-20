
#Kicad pin type definitions, mapped to human-readable descriptions
KICAD_PIN_TYPES_MAP = {
    "I" : "Input",
    "O" : "Output",
    "B" : "Bidirectional",
    "T" : "Tristate",
    "P" : "Passive",
    "U" : "Unspecified",
    "W" : "Power Input",
    "w" : "Power Output",
    "C" : "Open Collector",
    "E" : "Open Emitter",
    "N" : "No Connect",
}

#simple list of allowable KiCad pin types 
KICAD_PIN_TYPES = KICAD_PIN_TYPES_MAP.keys()

KICAD_PIN_DIRS_MAP = {
    'L' : 'Left',
    'R' : 'Right',
    'U' : 'Up',
    'D' : 'Down',
}

KICAD_PIN_DIRS = KICAD_PIN_DIRS_MAP.keys()

KICAD_PIN_STYLES_MAP = {
    '' : 'Normal',
    'I' : 'Inverted',
    'C' : 'Clock',
    'L' : 'Input Low',
    'CL' : 'Clock Low',
    'V' : 'Output Low',
    'F' : 'Falling Edge Clock',
    'X' : 'Non-logic'
}

KICAD_PIN_STYLES = KICAD_PIN_STYLES_MAP.keys()

KICAD_SHAPE_FILLS_MAP = {
    'N' : 'No Fill',
    'F' : 'Foreground',
    'f' : 'Background',
}

KICAD_SHAPE_FILLS = KICAD_SHAPE_FILLS_MAP.keys()


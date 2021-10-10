"""
This file contains the code needed for dealing with some of the mappings. Usually a map is just a
dictionary that needs to be loaded inside a variable.
This file carries the function to parse the files and the variables containing the dictionaries
themselves.
"""

import yaml

def load_mapping(filename):
    """
    Load a map from a file. The format must be something that resembles the python dictionary.abs
    We use the yaml library for that, as using eval() may be dangerous.
    It will return the data loaded as a dictionary.
    """

    with open(filename) as file:
        content = yaml.safe_load(file.read())

    return content

# Loaded data go here
tk_color_codes = load_mapping('maps/color_code_mapping.txt')
midi_notes = load_mapping('maps/midi_to_note_mapping.txt')
scale_notes = load_mapping('maps/note_to_midi_mapping.txt')
volume_positions =  load_mapping('maps/volume_positions.txt')
volume_colors = load_mapping('maps/volume_colors.txt')
pad_notes = load_mapping('maps/pad_notes.txt')
layouts = load_mapping('maps/layouts.txt')

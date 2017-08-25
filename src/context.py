import os
import mido
from mode import Mode
from launchpad_input import pad_notes
from launchpad_input import volume_positions
from launchpad_input import volume_colors

import launchpad_translator as t

def load_modes():
    """

    """
    all_modes = []

    for directory in os.listdir(r'modes'):
        full_dir = 'modes' + os.sep + directory
        if os.path.isdir(full_dir):
            all_modes.append(Mode(full_dir))

    return all_modes

modes = load_modes()
current_mode_position = 0
current_mode = modes[current_mode_position]
current_volume = 100
current_volume_pos = 47

def cycle_mode(midiout):
    global current_mode_position
    global current_mode

    current_mode_position += 1

    if current_mode_position >= len(modes):
        current_mode_position = 0

    modes[current_mode_position].refresh_background(midiout)

    current_mode = modes[current_mode_position]

def next_mode(midiout):
    global current_mode_position
    global current_mode

    if current_mode_position < len(modes)-1:
        current_mode_position += 1
        modes[current_mode_position].refresh_background(midiout)

        current_mode = modes[current_mode_position]


def previous_mode(midiout):
    global current_mode_position
    global current_mode

    if current_mode_position > 0:
        current_mode_position -= 1
        modes[current_mode_position].refresh_background(midiout)

        current_mode = modes[current_mode_position]

def increase_volume():
    global current_volume
    global current_volume_pos

    old_volume = current_volume_pos

    if current_volume_pos < 63:
        current_volume_pos += 1

    current_volume = volume_positions[current_volume_pos]

    return not current_volume_pos == old_volume

def decrease_volume():
    global current_volume
    global current_volume_pos

    old_volume = current_volume_pos
    
    if current_volume_pos > 0:
        current_volume_pos -= 1

    current_volume = volume_positions[current_volume_pos]

    return not current_volume_pos == old_volume

def display_volume_meeter(midiout):

    for note, index in zip(pad_notes[0:current_volume_pos+1], range(current_volume_pos+1)):

        # Send the message
        t.light_on_color_code(midiout, note, volume_colors[index])

    for note, index in zip(pad_notes[current_volume_pos+1:], range(current_volume_pos+1, 64)):

        # Send the message
        t.light_on_color_code(midiout, note, 0)

def set_volume(note):
    global current_volume
    global current_volume_pos

    note_index = pad_notes.index(note)

    # define the volume
    current_volume_pos = note_index
    current_volume = volume_positions[current_volume_pos]

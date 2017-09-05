import os

from mode import Mode

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
favorites = [None, None]

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

def set_mode(midiout, mode):
    global current_mode_position
    global current_mode

    current_mode_position = mode
    modes[current_mode_position].refresh_background(midiout)
    current_mode = modes[current_mode_position]
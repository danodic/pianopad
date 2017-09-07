import map_manager as maps
import translator as t

current_volume = 100
current_volume_pos = 47
favorites = [None, None]

def increase_volume():
    global current_volume
    global current_volume_pos

    old_volume = current_volume_pos

    if current_volume_pos < 63:
        current_volume_pos += 1

    current_volume = maps.volume_positions[current_volume_pos]

    return not current_volume_pos == old_volume

def decrease_volume():
    global current_volume
    global current_volume_pos

    old_volume = current_volume_pos
    
    if current_volume_pos > 0:
        current_volume_pos -= 1

    current_volume = maps.volume_positions[current_volume_pos]

    return not current_volume_pos == old_volume

def display_volume_meeter(midiout):

    for note, index in zip(maps.pad_notes[0:current_volume_pos+1], range(current_volume_pos+1)):

        # Send the message
        t.light_on_color_code(midiout, note, maps.volume_colors[index])

    for note, index in zip(maps.pad_notes[current_volume_pos+1:], range(current_volume_pos+1, 64)):

        # Send the message
        t.light_on_color_code(midiout, note, 0)

def set_volume(note):
    global current_volume
    global current_volume_pos

    note_index = maps.pad_notes.index(note)

    # define the volume
    current_volume_pos = note_index
    current_volume = maps.volume_positions[current_volume_pos]

def set_volume_position(pos):
    global current_volume
    global current_volume_pos

    # define the volume
    current_volume_pos = pos
    current_volume = maps.volume_positions[current_volume_pos]

import keyboard

color_map = []

key_mapping = {
}

modifiers = ['ctrl', 'shift', 'alt', 'fn', 'altgr']
active_keys = []

def release_key(note):

    key = key_mapping[note]

    if key in active_keys:
        active_keys.remove(key)

    print("release " + key)

    # Send the keystroke
    keyboard.send(key, False, True)

def press_key(note):

    actual_key = ''

    # Get the key
    key = key_mapping[note]

    # Check if this is a modifier
    if key not in active_keys:
        active_keys.append(key)

    # Add the modifiers
    for mod in active_keys:
        actual_key += mod + '+'

    # Check if we have added modifiers
    if len(actual_key) > 0:
        actual_key = actual_key[:-1]

    print("press " + actual_key)

    # Send the keystroke
    keyboard.send(actual_key, True, False)

def load_keyboard_mapping():

    with open('keyboard/keyboard.txt') as file:
        for row in file:
            key, value = row.split(':')
            if value.strip() != '':
                key_mapping[int(key)] = value.strip()

def load_color_mapping():

    global color_map

    with open('keyboard/colors.txt') as file:
        for file_row in file:
            array_row = []
            colors = file_row.split(',')
            
            for color in colors:
                array_row.append(int(color.strip()))

            color_map.append(array_row)

def refresh_background(launchpad):

        color = list(reversed(color_map))

        # Go over the screen array and draw it
        for row in range(8):
            for column in range(8):

                # Transform the coordinate into the proper note
                to_note = ((row+1) * 10) + (column+1)

                # Send the message
                launchpad.light_on_color_code(to_note, color[row][column])

load_keyboard_mapping()
load_color_mapping()

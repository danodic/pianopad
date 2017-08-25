import context

def main_screen_panel():
    
    # Buttons are red when cannot move anymore
    if context.current_mode.max_row == context.current_mode.current_row:
        up_button = [40, 0, 0]
    
    else:
        up_button = [0, 40, 0]

    if context.current_mode.current_row == 0:
        down_button = [40, 0, 0]
    
    else:
        down_button = [0, 40, 0]

    if context.current_mode.current_root_note == 0:
        left_button = [40, 0, 0]
    
    else:
        left_button = [0, 40, 0]
    
    if context.current_mode.current_root_note == int(context.current_mode.properties['octave size']) - 1:
        right_button = [40, 0, 0]
    
    else:
        right_button = [0, 40, 0]

    if len(context.modes) > 0:
        session_button = [0, 40, 0]
    else:
        session_button = [0, 0, 0]

    return [up_button, down_button, left_button, right_button, session_button, None, None, None]
    
def volume_key_panel():

    if context.current_volume == 127:
        up_button = [63, 0, 0]
    else:
        up_button = [0, 63, 0]

    if context.current_volume == 0:
        down_button = [63, 0, 0]
    else:
        down_button = [0, 63, 0]

    return [up_button, down_button, None, None, None, None, None, None]
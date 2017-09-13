import mode_manager as mom
import controller as ctrl

def main_screen_panel():
    
    # Buttons are red when cannot move anymore
    if mom.current_mode.max_row == mom.current_mode.current_row:
        up_button = [40, 0, 0]
    
    else:
        up_button = [0, 40, 0]

    if mom.current_mode.current_row == 0:
        down_button = [40, 0, 0]
    
    else:
        down_button = [0, 40, 0]

    if mom.current_mode.current_root_note == 0:
        left_button = [40, 0, 0]
    
    else:
        left_button = [0, 40, 0]
    
    if mom.current_mode.current_root_note == int(mom.current_mode.properties['octave size']) - 1:
        right_button = [40, 0, 0]
    
    else:
        right_button = [0, 40, 0]

    if len(mom.modes) > 0:
        session_button = [0, 40, 0]
    else:
        session_button = [0, 0, 0]

    if mom.favorites[0] is None:
        user1_button = [63, 0, 0]
    elif mom.favorites[0] == mom.current_mode:
        user1_button = [63, 0, 0]
    else:
        user1_button = [0, 0, 63]

    if mom.favorites[1] is None:
        user2_button = [63, 0, 0]
    elif mom.favorites[1] == mom.current_mode:
        user1_button = [63, 0, 0]
    else:
        user2_button = [0, 0, 63]

    return [up_button, down_button, left_button, right_button, session_button, user1_button, user2_button, None]

def main_screen_side_panel():

    record_arm = [40, 40, 40]

    return [volume_key(), None, None, None, None, None, None, record_arm]

def volume_key_panel():

    if ctrl.current_volume == 127:
        up_button = [63, 0, 0]
    
    else:
        up_button = [0, 63, 0]


    if ctrl.current_volume == 0:
        down_button = [63, 0, 0]
    
    else:
        down_button = [0, 63, 0]


    if ctrl.favorites[0] is None:
        user1_button = [63, 0, 0]
    
    else:
        user1_button = [0, 0, 63]


    if ctrl.favorites[1] is None:
        user2_button = [63, 0, 0]

    else:
        user2_button = [0, 0, 63]


    return [up_button, down_button, None, None, None, user1_button, user2_button, None]

def volume_side_panel():

    return [volume_key(), None, None, None, None, None, None, None]

def mode_selection_panel():
    
    session_button = [63, 63, 63]

    if mom.current_mode_position == 0:
        left_button = [63,0,0]
    else:
        left_button = [0,63,0]

    if mom.current_mode_position < len(mom.modes)-1:
        right_button = [0,63,0]
    else:
        right_button = [63,0,0]

    if mom.favorites[0] is None:
        user1_button = [63, 0, 0]
    elif mom.favorites[0] == mom.current_mode:
        user1_button = [63, 0, 0]
    else:
        user1_button = [0, 0, 63]

    if mom.favorites[1] is None:
        user2_button = [63, 0, 0]
    elif mom.favorites[1] == mom.current_mode:
        user1_button = [63, 0, 0]
    else:
        user2_button = [0, 0, 63]

    return [None, None, left_button, right_button, session_button, user1_button, user2_button, None]

def shift_main_panel():

    session_button = [63, 63, 63]

    if mom.current_mode.padding > 0:
        left_button = [0,63,0]
    else:
        left_button = [63,0,0]

    if mom.current_mode.padding < 8:
        right_button = [0,63,0]
    else:
        right_button = [63,0,0]

    return [None, None, left_button, right_button, None, None, None, None]

def shift_main_side():

    record_arm = [63, 25, 0]

    return [None, None, None, None, None, None, None, record_arm]

def volume_key():

    if ctrl.current_volume > 100:
        volume_button = [63, 0, 0]
    
    elif ctrl.current_volume == 100:
        volume_button = [63, 25, 0]
    
    else:
        volume_button = [0, int((63*ctrl.current_volume)/99), 0]

    return volume_button
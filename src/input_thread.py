import threading
import time

import translator as t
import panels
import keyboard
import keyboard_manager
import mode_manager as mom
import controller as ctrl
import launchpad

from map_manager import pad_notes
from keyboard_manager import key_mapping
from keyboard_manager import press_key, release_key


class InputThread (threading.Thread):
    """
    
    """

    def __init__(self, midiout_external = None):
        """
        TODO
        """

        self.ui = None

        self.default_timeout = 0.0001
        self.volume_change_timeout = 0.1

        # Initialize the threading lib
        threading.Thread.__init__(self)

        # Store some variables
        self.launchpad = None
        self.midiout_external = midiout_external
        self.midiout_launchpad = None
        self.keep_running = True
        self.running = False

        # Defines the current screen
        self.current_screen = 'main'
        #self.screens = {
        #    'main': screen_main()
        #}

    def run(self):
        self.wait_for_midi_devices()

        if not self.keep_running:
            return

        self.running = True
        self.screen_main()

    def wait_for_midi_devices(self):
        while (self.launchpad is None or self.midiout_external is None) and self.keep_running:
            time.sleep(self.default_timeout)

    def open_launchpad(self, input_name, output_name):
        self.launchpad = launchpad.create(input_name, output_name)
        self.midiout_launchpad = self.launchpad.midiout

    def screen_main(self):
        """

        """

        self.light_upper_panel(panels.main_screen_panel())
        self.light_right_panel(panels.main_screen_side_panel())

        mom.current_mode.refresh_background(self.launchpad)

        while self.keep_running:
           
            # Get the message
            message = self.launchpad.poll()
            
            if message:

                # Organize the values
                data = message.dict()

                # Pad note
                if data['type'] in ['note_on', 'note_off'] and data['note'] in pad_notes:
                    
                    if data['velocity'] == 127:
                        mom.current_mode.play_note(data['note'], ctrl.current_volume, self.midiout_external, self.launchpad)
                    
                    else:
                        mom.current_mode.release_note(data['note'], self.midiout_external, self.launchpad)

                # Panel keys
                elif data['type'] == 'control_change' and data['control'] in self.launchpad.function_keys:
                    
                    # ^
                    if data['control'] == 104 and data['value'] == 127:
                        mom.current_mode.move_up()
                        mom.current_mode.refresh_background(self.launchpad)
                        self.ui.color_buttons()
                    
                    # v
                    elif data['control'] == 105 and data['value'] == 127:
                        mom.current_mode.move_down()
                        mom.current_mode.refresh_background(self.launchpad)
                        self.ui.color_buttons()
                    
                    # <
                    elif data['control'] == 106 and data['value'] == 127:
                        mom.current_mode.root_note_down()
                        mom.current_mode.refresh_background(self.launchpad)
                        self.ui.color_buttons()

                    # >
                    elif data['control'] == 107 and data['value'] == 127:
                        mom.current_mode.root_note_up()
                        mom.current_mode.refresh_background(self.launchpad)
                        self.ui.color_buttons()

                    # Session
                    elif data['control'] == 108 and data['value'] == 127:
                        self.session_key()
                        self.ui.color_buttons()
                        self.ui.update_current_mode_name()

                    # User 1
                    elif data['control'] == 109 and data['value'] == 127:
                        if mom.favorites[0] != None:
                            mom.set_mode(self.launchpad, mom.favorites[0])
                            self.ui.update_current_mode_name()
                            self.ui.update_listbox()

                    # User 2
                    elif data['control'] == 110 and data['value'] == 127:
                        if mom.favorites[1] != None:
                            mom.set_mode(self.launchpad, mom.favorites[1])
                            self.ui.update_current_mode_name()
                            self.ui.update_listbox()

                    # Mixer button
                    elif data['control'] == 111 and data['value'] == 127:
                        self.mixer_key()

                    # Light up the panel after coming from another screen
                    self.light_upper_panel(panels.main_screen_panel())
                    self.light_right_panel(panels.main_screen_side_panel())

                # Side keys
                elif data['type'] == 'note_on' and data['note'] in self.launchpad.function_keys:
                    
                    # Volume
                    if data['note'] == 89 and data['type'] == 'note_on':
                        self.volume_key()

                    # Shift
                    if data['note'] == 19 and data['type'] == 'note_on':
                        self.shift_key()

                    # Light up the panel after coming from another screen
                    self.light_upper_panel(panels.main_screen_panel())
                    self.light_right_panel(panels.main_screen_side_panel())
                        
            time.sleep(self.default_timeout)

    def session_key(self):

        # Session button:
        # Tap: switch to the next mode
        # Hold: highlight horizontal arrows, move between modes

        # Light the upper panel
        self.light_upper_panel(panels.mode_selection_panel())

        # Store if we have pressed any arrow, so we can identify the tap
        key_pressed = False
        
        # Get into this key's loop
        while True:

            # Poll message
            message = self.launchpad.poll()
            
            # Do Stuff in case of message
            if message:
            
                data = message.dict()

                # Loop deactivation
                if data['type'] == 'control_change' and data['control'] == 108 and data['value'] == 00:

                    # Tap
                    if not key_pressed:
                        mom.cycle_mode(self.launchpad)
                        self.ui.update_listbox()
                        break

                    else:
                        break

                # Hold + <: Move to the previous mode
                elif data['type'] == 'control_change' and data['control'] == 106 and data['value'] == 127:
                    mom.previous_mode(self.launchpad)
                    key_pressed = True

                    # Update panel
                    self.light_upper_panel(panels.mode_selection_panel())
                    self.ui.update_listbox()

                # Hold + >: Move to the next mode
                elif data['type'] == 'control_change' and data['control'] == 107 and data['value'] == 127:
                    mom.next_mode(self.launchpad)
                    key_pressed = True

                    # Update panel
                    self.light_upper_panel(panels.mode_selection_panel())
                    self.ui.update_listbox()

                # Hold User 1
                elif data['type'] == 'control_change' and data['control'] == 109 and data['value'] == 127:
                
                    key_pressed = True                    

                    if self.check_hold(109):
                        mom.favorites[0] = mom.current_mode_position
                        self.ui.update_user_1_mode_name()

                # Hold User 2
                elif data['type'] == 'control_change' and data['control'] == 110 and data['value'] == 127:

                    key_pressed = True
                    
                    if self.check_hold(110):
                        mom.favorites[1] = mom.current_mode_position
                        self.ui.update_user_2_mode_name()

                # Light the upper panel
                self.light_upper_panel(panels.mode_selection_panel())

            time.sleep(self.default_timeout)

    def volume_key(self):

        # Volume key
        # Will display a meter from the first button up until the last one.
        # The arrows (up and down) will increase and decrease the volume.
        # As the user keeps the button pressed, it will sum a certain amount to
        # the volume. This will gradually fill the meeter.

        # Display the volume meeter
        ctrl.display_volume_meeter(self.launchpad)

        # Light the upper panel
        self.light_upper_panel(panels.volume_key_panel())
        
        # Get into this key's loop
        while True:

            # Poll message
            message = self.launchpad.poll()
            
            # Do Stuff in case of message
            if message:
            
                data = message.dict()

                # Loop deactivation
                if data['type'] == 'note_on' and data['note'] == 89 and data['velocity'] == 0:
                    mom.current_mode.refresh_background(self.launchpad)
                    break

                if data['type'] == 'note_on' and data['note'] in pad_notes:
                    ctrl.set_volume(data['note'])
                    ctrl.display_volume_meeter(self.launchpad)
                    self.light_right_panel(panels.volume_side_panel())
                    self.ui.update_volume()

                # Hold + ^: Increase volume
                elif data['type'] == 'control_change' and data['control'] == 104 and data['value'] == 127:
                    self.increase_volume()

                # Hold + v: Decrease volume
                elif data['type'] == 'control_change' and data['control'] == 105 and data['value'] == 127:
                    self.decrease_volume()

                # Hold User 1
                elif data['type'] == 'control_change' and data['control'] == 109 and data['value'] == 127:            

                    if self.check_hold(109):
                        ctrl.favorites[0] = ctrl.current_volume_pos
                        ctrl.display_volume_meeter(self.launchpad)
                        self.ui.update_user_1_volume()
                        self.light_upper_panel(panels.volume_key_panel())

                    elif ctrl.favorites[0] != None:
                        ctrl.current_volume_pos = ctrl.favorites[0]
                        ctrl.display_volume_meeter(self.launchpad)
                        self.ui.update_volume()

                # Hold User 2
                elif data['type'] == 'control_change' and data['control'] == 110 and data['value'] == 127:
                    
                    if self.check_hold(110):
                        ctrl.favorites[1] = ctrl.current_volume_pos
                        ctrl.display_volume_meeter(self.launchpad)
                        self.ui.update_user_2_volume()
                        self.light_upper_panel(panels.volume_key_panel())

                    elif ctrl.favorites[1] != None:
                        ctrl.current_volume_pos = ctrl.favorites[1]
                        ctrl.display_volume_meeter(self.launchpad)
                        self.ui.update_volume()

                # Light the upper panel
                self.light_upper_panel(panels.volume_key_panel())

            time.sleep(self.default_timeout)

    def mixer_key(self):

        keyboard_manager.refresh_background(self.launchpad)

        while self.keep_running:
           
            # Get the message
            message = self.launchpad.poll()
            
            if message:

                # Organize the values
                data = message.dict()

                # Pad note
                if data['type'] in ['note_on'] and data['note'] in key_mapping:

                    if data['velocity'] == 127:
                        press_key(data['note'])

                    elif data['velocity'] == 00:
                        release_key(data['note'])

                # Mixer button
                elif data['type'] == 'control_change':
                    
                    if data['control'] == 111 and data['value'] == 127:
                        break

            time.sleep(self.default_timeout)

        mom.current_mode.refresh_background(self.launchpad)

    def shift_key(self):

        # Light the panel
        self.light_upper_panel(panels.shift_main_panel())
        self.light_right_panel(panels.shift_main_side())

        while self.keep_running:
           
            # Get the message
            message = self.launchpad.poll()
            
            if message:

                # Organize the values
                data = message.dict()

                # Leave shift mode
                if data['type'] in ['note_on'] and data['note'] == 19:

                    if data['velocity'] == 00:
                        return

                # Slide <
                elif data['type'] == 'control_change' and data['control'] == 106 and data['value'] == 127:
                    mom.current_mode.slide_left()
                    mom.current_mode.refresh_background(self.launchpad)
                    self.ui.color_buttons()
                    self.light_upper_panel(panels.shift_main_panel())

                # Slide >
                elif data['type'] == 'control_change' and data['control'] == 107 and data['value'] == 127:
                    mom.current_mode.slide_right()
                    mom.current_mode.refresh_background(self.launchpad)
                    self.ui.color_buttons()
                    self.light_upper_panel(panels.shift_main_panel())

            time.sleep(self.default_timeout)

        mom.current_mode.refresh_background(self.launchpad)

    def increase_volume(self):

        # Light up the ^ button
        t.light_on(self.midiout_launchpad, 104, 63, 16, 0)

        # Wait for the button to be released
        while True:
            
            # Poll message
            message = self.launchpad.poll()

            if message:

                data = message.dict()

                if data['type'] == 'control_change' and data['control'] == 104 and data['value'] == 00:
                    break

            if ctrl.increase_volume():
                ctrl.display_volume_meeter(self.launchpad)
                self.light_right_panel(panels.volume_side_panel())
                self.ui.update_volume()

            time.sleep(self.volume_change_timeout)

        # Light off the ^ button
        t.light_off(self.midiout_launchpad, 104)

    def decrease_volume(self):
        # Wait for the button to be released
        while True:

            # Poll message
            message = self.launchpad.poll()

            if message:

                data = message.dict()
                
                if data['type'] == 'control_change' and data['control'] == 105 and data['value'] == 00:
                    break

            if ctrl.decrease_volume():
                ctrl.display_volume_meeter(self.launchpad)
                self.light_right_panel(panels.volume_side_panel())
                self.ui.update_volume()

            time.sleep(self.volume_change_timeout)

    def light_upper_panel(self, lights = [None, None, None, None, None, None, None, None]):
    
        for light, note in zip(lights, range(104, 112)):
            if light is None:
                t.light_off(self.midiout_launchpad, note)

            else:
                # Light up the button
                t.light_on(self.midiout_launchpad, note, light[0], light[1], light[2])

    def light_right_panel(self, lights = [None, None, None, None, None, None, None, None]):
    
        for light, note in zip(lights, [89, 79, 69, 59, 49, 39, 29, 19]):
            if light is None:
                t.light_off(self.midiout_launchpad, note)

            else:
                # Light up the button
                t.light_on(self.midiout_launchpad, note, light[0], light[1], light[2])


    def light_panel_button(self, button, color):
         
         # Light up the button
        t.light_on(self.midiout_launchpad, button, color[0], color[1], color[2])

    def check_hold(self, note):
        
        # Set the starting time
        start_time = time.time()

        while True:
        
            # Poll message
            message = self.launchpad.poll()
            
            # Check if time elapsed
            if (time.time() - start_time) >= 3:
                return True;

            # Do Stuff in case of message
            if message:

                data = message.dict()

                # Release key
                if data['type'] == 'control_change' and data['control'] == note and data['value'] == 0:
                    return False

        time.sleep(self.default_timeout)

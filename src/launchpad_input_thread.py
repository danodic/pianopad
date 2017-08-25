import pdb

import threading
import time
import context
from launchpad_input import pad_notes
import launchpad_translator as t
import panels

class LaunchpadInputThread (threading.Thread):
    """
    
    """

    def __init__(self, midiin, midiout_launchpad, midiout_external):
        """
        TODO
        """

        self.default_timeout = 0.001
        self.volume_change_timeout = 0.1

        # Initialize the threading lib
        threading.Thread.__init__(self)

        # Store some variables
        self.midiin = midiin
        self.midiout_external = midiout_external
        self.midiout_launchpad = midiout_launchpad
        self.keep_running = True

        # Defines the function keys
        self.function_keys = [89,104, 105, 106, 107, 108, 109, 110, 111]

        # Defines the current screen
        self.current_screen = 'main'
        #self.screens = {
        #    'main': screen_main()
        #}

    def run(self):
        # Run the default screen
        #self.screens[self.current_screen]()
        self.screen_main()

    def screen_main(self):
        """

        """

        self.light_upper_panel(panels.main_screen_panel())
        context.current_mode.refresh_background(self.midiout_launchpad)

        while self.keep_running:
           
            # Get the message
            message = self.midiin.poll()
            
            if message:

                # Organize the values
                data = message.dict()

                if data['type'] in ['note_on', 'note_off'] and data['note'] in pad_notes:
                    
                    if data['velocity'] == 127:
                        context.current_mode.play_note(data['note'], context.current_volume, self.midiout_external, self.midiout_launchpad)
                    else:
                        context.current_mode.release_note(data['note'], self.midiout_external, self.midiout_launchpad)

                elif data['type'] == 'control_change' and data['control'] in self.function_keys:
                    if data['control'] == 104 and data['value'] == 127:
                        context.current_mode.move_up()
                        context.current_mode.refresh_background(self.midiout_launchpad)

                    elif data['control'] == 105 and data['value'] == 127:
                        context.current_mode.move_down()
                        context.current_mode.refresh_background(self.midiout_launchpad)
                    
                    elif data['control'] == 106 and data['value'] == 127:
                        context.current_mode.root_note_down()
                        context.current_mode.refresh_background(self.midiout_launchpad)

                    elif data['control'] == 107 and data['value'] == 127:
                        context.current_mode.root_note_up()
                        context.current_mode.refresh_background(self.midiout_launchpad)

                    elif data['control'] == 108 and data['value'] == 127:
                        self.session_key()

                    self.light_upper_panel(panels.main_screen_panel())

                elif data['type'] == 'note_on' and data['note'] in self.function_keys:
                    
                    if data['note'] == 89 and data['type'] == 'note_on':
                        self.volume_key()

                    self.light_upper_panel(panels.main_screen_panel())
                        
            time.sleep(self.default_timeout)

    def session_key(self):

        # Session button:
        # Tap: switch to the next mode
        # Hold: highlight horizontal arrows, move between modes

        # Store if we have pressed any arrow, so we can identify the tap
        arrow_pressed = False
        
        # Get into this key's loop
        while True:

            # Poll message
            message = self.midiin.poll()
            
            # Do Stuff in case of message
            if message:
            
                data = message.dict()

                # Loop deactivation
                if data['type'] == 'control_change' and data['control'] == 108 and data['value'] == 00:

                    # Tap
                    if not arrow_pressed:
                        context.cycle_mode(self.midiout_launchpad)
                        break

                    else:
                        break

                # Hold + <: Move to the previous mode
                elif data['type'] == 'control_change' and data['control'] == 106 and data['value'] == 127:
                    context.previous_mode(self.midiout_launchpad)
                    arrow_pressed = True

                # Hold + >: Move to the next mode
                elif data['type'] == 'control_change' and data['control'] == 107 and data['value'] == 127:
                    context.next_mode(self.midiout_launchpad)
                    arrow_pressed = True

            time.sleep(self.default_timeout)

    def volume_key(self):

        # Volume key
        # Will display a meter from the first button up until the last one.
        # The arrows (up and down) will increase and decrease the volume.
        # As the user keeps the button pressed, it will sum a certain amount to
        # the volume. This will gradually fill the meeter.

        # Display the volume meeter
        context.display_volume_meeter(self.midiout_launchpad)

        # Light the upper panel
        self.light_upper_panel(panels.volume_key_panel())
        
        # Get into this key's loop
        while True:

            # Poll message
            message = self.midiin.poll()
            
            # Do Stuff in case of message
            if message:
            
                data = message.dict()

                # Loop deactivation
                if data['type'] == 'note_on' and data['note'] == 89 and data['velocity'] == 0:
                    context.current_mode.refresh_background(self.midiout_launchpad)
                    break

                if data['type'] == 'note_on' and data['note'] in pad_notes:
                    context.set_volume(data['note'])
                    context.display_volume_meeter(self.midiout_launchpad)
                    self.light_upper_panel(panels.volume_key_panel())

                # Hold + ^: Increase volume
                elif data['type'] == 'control_change' and data['control'] == 104 and data['value'] == 127:
                    self.increase_volume()
                    self.light_upper_panel(panels.volume_key_panel())

                # Hold + v: Decrease volume
                elif data['type'] == 'control_change' and data['control'] == 105 and data['value'] == 127:
                    self.decrease_volume()
                    self.light_upper_panel(panels.volume_key_panel())

            time.sleep(self.default_timeout)

    def increase_volume(self):

        # Light up the ^ button
        t.light_on(self.midiout_launchpad, 104, 63, 16, 0)

        # Wait for the button to be released
        while True:
            
            # Poll message
            message = self.midiin.poll()

            if message:

                data = message.dict()

                if data['type'] == 'control_change' and data['control'] == 104 and data['value'] == 00:
                    break

            if context.increase_volume():
                context.display_volume_meeter(self.midiout_launchpad)

            time.sleep(self.volume_change_timeout)

        # Light off the ^ button
        t.light_off(self.midiout_launchpad, 104)

    def decrease_volume(self):
        # Wait for the button to be released
        while True:

            # Poll message
            message = self.midiin.poll()

            if message:

                data = message.dict()
                
                if data['type'] == 'control_change' and data['control'] == 105 and data['value'] == 00:
                    break

            if context.decrease_volume():
                context.display_volume_meeter(self.midiout_launchpad)

            time.sleep(self.volume_change_timeout)

    def light_upper_panel(self, lights = [None, None, None, None, None, None, None, None]):
    
        for light, note in zip(lights, range(104, 112)):
            if light is None:
                t.light_off(self.midiout_launchpad, note)

            else:
                # Light up the button
                t.light_on(self.midiout_launchpad, note, light[0], light[1], light[2])
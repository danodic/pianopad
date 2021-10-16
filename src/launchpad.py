import mido
import midi_manager
import re


def create(input_name, output_name):
    midiin = midi_manager.get_input_port(input_name)
    midiout = midi_manager.get_output_port(output_name)
    # this is possibly an overly simplistic method to detect the device type
    if re.match('^Launchpad Mini', input_name):
        return LaunchpadMiniMk2(midiin, midiout)
    else:
        return LaunchpadMk2(midiin, midiout)


class Launchpad:
    def __init__(self, midiin, midiout):
        self.midiin = midiin
        self.midiout = midiout

    def poll(self):
        return self.midiin.poll()


class LaunchpadMk2(Launchpad):
    # This is the default sysex header for launchpad MK2
    # It will translate to [F0, 00, 20, 29, 02, 18]
    default_header = [0,32,41,2,24]
    function_keys = [104, 105, 106, 107, 108, 109, 110, 111]
    pad_notes = [ (x//8)*10 + x%8 + 11 for x in range(64) ]
    side_keys = [ 89, 79, 69, 59, 49, 39, 29, 19 ]

    def light_on_color_code(self, key, color):
        # 10 = Set leds in color code mode
        message = mido.Message('sysex', data = self.default_header + [10] + [key, color])
        self.midiout.send(message)

    def light_on(self, key, r=63, g=63, b=63):
        # 11 = Set leds in RGB mode
        message = mido.Message('sysex', data = self.default_header + [11] + [key, r, g, b])
        self.midiout.send(message)

    def light_off(self, key):
        # 10 = Set leds in color code mode
        message = mido.Message('sysex', data = self.default_header + [10] + [key, 0])
        self.midiout.send(message)

    def light_all(self, color):
        # 14 = Set all leds
        message = mido.Message('sysex', data = self.default_header + [14] + [color])
        self.midiout.send(message)

    # the function key light on and off functions don't change for the Mk2
    fn_light_on = light_on
    fn_light_off = light_off

    @staticmethod
    def map_note_to_grid(note):
        '''Maps to input note value to the grid row & column'''
        row = int(note/10) - 1
        column = note % 10 - 1
        return (row, column)

    @staticmethod
    def map_grid_to_note(row, column):
        '''Maps the grid row & column to a note'''
        return ((row+1) * 10) + (column+1)


class LaunchpadMiniMk2(Launchpad):
    function_keys = [104, 105, 106, 107, 108, 109, 110, 111]
    pad_notes = [ (7-(x//8))*16 + x%8 for x in range(64) ]
    side_keys = [ 8, 24, 40, 56, 72, 88, 104, 120 ]

    @staticmethod
    def _map_color(color):
        # map colors to rg velocity
        if color == 0:
            red=0
            green=0
        elif color in (5, 6):
            red=3
            green=0
        else:
            red=1
            green=1
        return red+green*16

    @staticmethod
    def _map_rgb(r, g, b):
        # map the rgb to a rg color
        red=r//32
        green=max(g,b)//32
        return red+green*16

    def light_on_color_code(self, key, color):
        message =  mido.Message('note_on', note=key, velocity = self._map_color(color))
        self.midiout.send(message)

    def light_on(self, key, r=63, g=63, b=63):
        message =  mido.Message('note_on', note=key, velocity = self._map_rgb(r,g,b))
        self.midiout.send(message)

    def light_off(self, key):
        # velocity 0 to turn lights off
        message =  mido.Message('note_off', note=key, velocity = 0)
        self.midiout.send(message)

    def light_all(self, color):
        # there is no real equivalent for the light_all command with a color
        # 0x7d, 0x7e, 0x7f set all leds at dim, medium, bright
        # 0 is reset, which is a bit brutal perhaps
        print('light_all', color)
        #message = mido.Message('control_change', value = 0x7d)
        message = mido.Message('control_change', value = 0)
        self.midiout.send(message)

    def fn_light_on(self, key, r=63, g=63, b=63):
        if key in self.function_keys:
            message =  mido.Message('control_change', control=key, value=self._map_rgb(r,g,b))
            self.midiout.send(message)

    def fn_light_off(self, key):
        # velocity 0 to turn lights off
        if key in self.function_keys:
            message =  mido.Message('control_change', control=key, value=0)
            self.midiout.send(message)

    @staticmethod
    def map_note_to_grid(note):
        '''Maps to input note value to the grid row & column'''
        row = 7 - (note//16)
        column = note%16
        return (row, column)

    @staticmethod
    def map_grid_to_note(row, column):
        '''Maps the grid row & column to a note'''
        return (7-row) * 16 + column

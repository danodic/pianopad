import mido

# This is the default sysex header for launchpad MK2
# It will translate to [F0, 00, 20, 29, 02, 18]
default_header = [0,32,41,2,24]

def note_on(midiout, note, velocity = 100):
    message =  mido.Message('note_on', note=note, velocity = velocity)
    midiout.send(message)

def note_off(midiout, note):
    message =  mido.Message('note_off', note=note)
    midiout.send(message)

def light_on_color_code(midiout, key, color):
    # 10 = Set leds in color code mode
    message = mido.Message('sysex', data = default_header + [10] + [key, color])
    midiout.send(message)

def light_on(midiout, key, r=63, g=63, b=63):
    # 11 = Set leds in RGB mode
    message = mido.Message('sysex', data = default_header + [11] + [key, r, g, b])
    midiout.send(message)

def light_off(midiout, key):
    # 10 = Set leds in color code mode
    message = mido.Message('sysex', data = default_header + [10] + [key, 0])
    midiout.send(message)

def light_all(midiout, color):
    # 14 = Set all leds
    message = mido.Message('sysex', data = default_header + [14] + [color])
    midiout.send(message)
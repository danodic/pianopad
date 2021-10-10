import mido

from map_manager import midi_notes

def note_on(midiout, note, velocity = 100):
    message =  mido.Message('note_on', note=note, velocity = velocity)
    midiout.send(message)

def note_off(midiout, note):
    message =  mido.Message('note_off', note=note)
    midiout.send(message)

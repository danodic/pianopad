
import midi_manager

def create(input_name, output_name):
    midiin = midi_manager.get_input_port(input_name)
    midiout = midi_manager.get_output_port(output_name)
    return Launchpad(midiin, midiout)

class Launchpad:
    def __init__(self, midiin, midiout):
        self.midiin = midiin
        self.midiout = midiout

    def poll(self):
        return self.midiin.poll()

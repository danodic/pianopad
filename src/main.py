import mido
import time
import sys

from mode import Mode
from launchpad_input_thread import LaunchpadInputThread

midiout_launchpad = None
midiout_external = None
midiin = None

def parse_devices():
    global midiout_launchpad
    global midiout_external
    global midiin

    with open('devices.txt') as file:
        
        for row in file:
            device_type, device_name = row.split(':')

            # Instantiate rtmidi
            if device_type.strip().lower() == 'input':
                midiin = mido.open_input(device_name.strip())

            elif device_type.strip().lower() == 'launchpad output':
                midiout_launchpad = mido.open_output(device_name.strip())

            elif device_type.strip().lower() == 'piano output':
                midiout_external = mido.open_output(device_name.strip())

    return True

def list_devices():
    print("output devices:")
    print(str(mido.get_output_names()))
    print("\ninput devices:")
    print(str(mido.get_input_names()))

# Check if we can start or if we need to list devices
if not parse_devices():
    list_devices()
    sys.exit(1)

print(midiout_launchpad.name)
print(midiout_external.name)
print(midiin.name)

# Launch the input thread
input_thread = LaunchpadInputThread(midiin, midiout_launchpad, midiout_external)
input_thread.daemon = True
input_thread.start()
input_thread.join()

# Wait for the inpur thread to finish
while True:
    time.sleep(1)
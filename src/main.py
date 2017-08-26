import mido
import time
import sys

from cefpython3 import cefpython as cef
import platform
import os

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

def check_versions():
    print("[hello_world.py] CEF Python {ver}".format(ver=cef.__version__))
    print("[hello_world.py] Python {ver} {arch}".format(
          ver=platform.python_version(), arch=platform.architecture()[0]))
    assert cef.__version__ >= "55.3", "CEF Python v55.3+ required to run this"

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

# Initialize the UI
check_versions()
sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
cef.Initialize()
cef.CreateBrowserSync(url=os.path.dirname(os.path.abspath(__file__)) + os.sep + r"ui\main.html",
                        window_title="Hello World!")
cef.MessageLoop()
cef.Shutdown()

input_thread.join()
from cx_Freeze import setup, Executable
import os

pythonpath = "T:\Programs\Python\Python310"

os.environ['TCL_LIBRARY'] = os.path.join(pythonpath, "tcl\\tcl8.6")
os.environ['TK_LIBRARY'] = os.path.join(pythonpath, "tcl\\tk8.6")

include_files=[os.path.join(pythonpath, "DLLs\\tcl86t.dll"),
               os.path.join(pythonpath, "DLLs\\tk86t.dll"),
               ".\\modes",
               ".\\keyboard",
               ".\\maps"]

base = None

executables = [Executable("main.py", base=base)]

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    'packages': ["tkinter","mido","rtmidi", "os","yaml","threading","time"],
    'include_files': include_files,
    'excludes': ['unittest', 'test']
}

# GUI applications require a different base on Windows
base = "Win32GUI"

setup (
    name = "pianopad",
    version = "0.2",
    description = "El perro, el perro, is mi corazon...",
    options = {"build_exe": build_exe_options},
    executables = [Executable("pianopad.py", base=base)]
)
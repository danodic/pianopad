from cx_Freeze import setup, Executable
import os

os.environ['TCL_LIBRARY'] = "C:\\Users\\danilo\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\danilo\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tk8.6"

include_files=["C:\\Users\\danilo\\AppData\\Local\\Programs\\Python\\Python36-32\\DLLs\\tcl86t.dll",
               "C:\\Users\\danilo\\AppData\\Local\\Programs\\Python\\Python36-32\\DLLs\\tk86t.dll"]

base = None

executables = [Executable("main.py", base=base)]

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    'packages': ["tkinter","mido","os","yaml","threading","time"],
    'include_files': include_files,
    'excludes': ['unittest', 'test']
}

# GUI applications require a different base on Windows
base = "Win32GUI"

setup (
    name = "pianopad",
    version = "0.1",
    description = "El perro, el perro, is mi corazon...",
    options = {"build_exe": build_exe_options},
    executables = [Executable("main.py", base=base)]
)
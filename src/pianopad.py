import tkinter as tk
from tkinter import ttk

from window_main import MainWindow
from input_thread import InputThread
import midi_manager as mm

# Initialize the input thread
input_thread = InputThread()

# Initialize the UI
root = tk.Tk()
root.wm_title("pianopad")
root.geometry("320x900")
app = MainWindow(input_thread, master=root)


# Assign the ui to the input thread
input_thread.ui = app
input_thread.daemon = True
input_thread.start()

# Wait for the input thread to finish
app.mainloop()
input_thread.keep_running = False
input_thread.join()

mm.close_open_ports()

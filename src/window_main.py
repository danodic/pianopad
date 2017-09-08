"""
This is the main window.
"""

import tkinter as tk
from tkinter import ttk

import midi_manager as mm
import mode_manager as mom
import map_manager as maps
import controller as ctrl

class MainWindow(tk.Frame):

    def __init__(self, input_thread, master=None):
        super().__init__(master)
        
        self.input_thread = input_thread

        self.create_variables()
        self.create_widgets()
        self.position_widgets()
        self.setup_widgets()
        self.add_callbacks()

        self.pack(fill=tk.BOTH)

    def create_variables(self):
        self.var_lp_input = tk.StringVar(self)
        self.var_lp_input.set("Select One")

        self.var_lp_output = tk.StringVar(self)
        self.var_lp_output.set("Select One")

        self.var_ext_output = tk.StringVar(self)
        self.var_ext_output.set("Select One")

        self.var_volume_scale = tk.IntVar(self)
        self.var_volume_scale.set(0)

        self.var_volume_scale_translated = tk.StringVar(self)

    def create_widgets(self):

        # Frames
        self.frame_midi = ttk.LabelFrame(self, text="Midi Settings")
        self.frame_modes = ttk.LabelFrame(self, text="Modes")
        self.frame_volume = ttk.LabelFrame(self, text="Volume")
        self.frame_status = ttk.LabelFrame(self, text="Status")
        self.frame_mapping = ttk.LabelFrame(self, text="Mapping")

        self.frame_status_mode = ttk.Frame(self.frame_status)
        self.frame_user1_mode = ttk.Frame(self.frame_status)
        self.frame_user2_mode = ttk.Frame(self.frame_status)
        self.frame_user1_volume = ttk.Frame(self.frame_status)
        self.frame_user2_volume = ttk.Frame(self.frame_status)

        # Labels
        self.label_lp_input = ttk.Label(self.frame_midi, text="Launchpad Input Device:")
        self.label_lp_output = ttk.Label(self.frame_midi, text="Launchpad Output Device:")
        self.label_ext_output = ttk.Label(self.frame_midi, text="External MIDI Output Device:")
        
        self.label_volume = ttk.Label(self.frame_volume, text="Volume:")
        self.label_volume_var = ttk.Label(self.frame_volume, textvariable=self.var_volume_scale_translated)

        self.label_current_mode = ttk.Label(self.frame_status_mode, text="Current Mode:")
        self.label_current_mode_var = ttk.Label(self.frame_status_mode, text="None")
        
        self.label_user1_mode = ttk.Label(self.frame_user1_mode, text="User 1 Mode:")
        self.label_user1_mode_var = ttk.Label(self.frame_user1_mode, text="Not Set")
        
        self.label_user2_mode = ttk.Label(self.frame_user2_mode, text="User 2 Mode:")
        self.label_user2_mode_var = ttk.Label(self.frame_user2_mode, text="Not Set")
        
        self.label_user1_volume = ttk.Label(self.frame_user1_volume, text="User 1 Volume:")
        self.label_user1_volume_var = ttk.Label(self.frame_user1_volume, text="Not SetA")
        
        self.label_user2_volume = ttk.Label(self.frame_user2_volume, text="User 2 Volume:")
        self.label_user2_volume_var = ttk.Label(self.frame_user2_volume, text="Not SetB")

        # Drop Downs
        self.dpw_lp_input = ttk.OptionMenu(self.frame_midi, self.var_lp_input, *(["Select One"] + mm.get_input_port_names()))
        self.dpw_lp_output = ttk.OptionMenu(self.frame_midi, self.var_lp_output, *(["Select One"] + mm.get_output_port_names()))
        self.dpw_ext_output = ttk.OptionMenu(self.frame_midi, self.var_ext_output, *(["Select One"] + mm.get_output_port_names()))

        # List Boxes
        self.scroll_modes = tk.Scrollbar(self.frame_modes, orient="vertical")

        self.lstb_listbox_modes = tk.Listbox(self.frame_modes, yscrollcommand=self.scroll_modes.set)
        for mode in mom.modes:
            self.lstb_listbox_modes.insert(tk.END, mode.properties['name'])
        
        self.scroll_modes.config(command=self.lstb_listbox_modes.yview)

        # Scales
        self.scale_volume = ttk.Scale(self.frame_volume, variable=self.var_volume_scale, from_=0, to=63, orient=tk.HORIZONTAL, command=self.callback_update_volume)

        # Buttons
        self.all_keys = []
        self.all_row_frames = []
        
        for row in range(8):
            current_row = []
            
            current_frame = ttk.Frame(self.frame_mapping)
            current_frame.pack(fill=tk.X)

            for column in range(8):
                new_button = tk.Button(current_frame, width="4", borderwidth=2, highlightcolor='white', relief=tk.FLAT)
                new_button.pack(side=tk.LEFT)
                current_row.append(new_button)

            self.all_row_frames.append(current_frame)
            self.all_keys.append(current_row)

    def position_widgets(self):

        # Midi Frame
        self.frame_midi.pack(fill=tk.X, padx=5, pady=5, ipadx=5, ipady=5)
        self.label_lp_input.pack(fill=tk.X, padx=5, pady=2)
        self.dpw_lp_input.pack(fill=tk.X, padx=5, pady=2)
        self.label_lp_output.pack(fill=tk.X, padx=5, pady=2)
        self.dpw_lp_output.pack(fill=tk.X, padx=5, pady=2)
        self.label_ext_output.pack(fill=tk.X, padx=5, pady=2)
        self.dpw_ext_output.pack(fill=tk.X, padx=5, pady=2)

        # Volume Frame
        self.frame_volume.pack(fill=tk.X, padx=5, pady=5, ipadx=5, ipady=5)
        self.scale_volume.pack(fill=tk.X, padx=5, pady=2)
        self.label_volume.pack(padx=5, pady=2, side=tk.LEFT)
        self.label_volume_var.pack(padx=5, pady=2, side=tk.LEFT)

        # Modes frame
        self.frame_modes.pack(fill=tk.X, padx=5, pady=5, ipadx=5, ipady=5)
        self.lstb_listbox_modes.pack(fill=tk.X, expand=1, side=tk.LEFT)
        self.scroll_modes.pack(fill=tk.Y, side=tk.RIGHT)

        # Status frame
        self.frame_status.pack(fill=tk.X, padx=5, pady=5, ipadx=5, ipady=5)

        self.frame_status_mode.pack(fill=tk.X)
        self.label_current_mode.pack(padx=5, pady=2, side=tk.LEFT)
        self.label_current_mode_var.pack(padx=5, pady=2, side=tk.LEFT)

        self.frame_user1_mode.pack(fill=tk.X)
        self.label_user1_mode.pack(padx=5, pady=2, side=tk.LEFT)
        self.label_user1_mode_var.pack(padx=5, pady=2, side=tk.LEFT)

        self.frame_user2_mode.pack(fill=tk.X)
        self.label_user2_mode.pack(padx=5, pady=2, side=tk.LEFT)
        self.label_user2_mode_var.pack(padx=5, pady=2, side=tk.LEFT)

        self.frame_user1_volume.pack(fill=tk.X)
        self.label_user1_volume.pack(padx=5, pady=2, side=tk.LEFT)
        self.label_user1_volume_var.pack(padx=5, pady=2, side=tk.LEFT)

        self.frame_user2_volume.pack(fill=tk.X)
        self.label_user2_volume.pack(padx=5, pady=2, side=tk.LEFT)
        self.label_user2_volume_var.pack(padx=5, pady=2, side=tk.LEFT)

        # Button matrix
        self.frame_mapping.pack(fill=tk.X, padx=5, pady=5, ipadx=5, ipady=5)

    def setup_widgets(self):
        self.color_buttons()
        self.update_volume()
        self.update_current_mode_name()
        self.update_user_1_mode_name()
        self.update_user_2_mode_name()
        self.update_user_1_volume()
        self.update_user_2_volume()
        self.update_listbox()

    def update_listbox(self):
        self.lstb_listbox_modes.selection_clear(0, tk.END)
        self.lstb_listbox_modes.selection_set(mom.current_mode_position)
        self.lstb_listbox_modes.see(mom.current_mode_position)

    def add_callbacks(self):
        self.var_lp_input.trace_add("write", self.callback_lp_input)
        self.var_lp_output.trace_add("write", self.callback_lp_output)
        self.var_ext_output.trace_add("write", self.callback_ext_output)

        self.lstb_listbox_modes.bind('<<ListboxSelect>>', self.callback_listbox_modes)

    def callback_update_volume(self, *args):
        ctrl.set_volume_position(self.var_volume_scale.get())
        self.var_volume_scale_translated.set(maps.volume_positions[int(self.var_volume_scale.get())])

    def callback_listbox_modes(self, event):
        if self.input_thread.running:
            index = int(event.widget.curselection()[0])
            mom.set_mode(self.input_thread.midiout_launchpad, index)
            self.color_buttons()

    def callback_lp_input(self, *args):
        self.input_thread.midiin = mm.get_input_port(self.var_lp_input.get())
    
    def callback_lp_output(self, *args):
        self.input_thread.midiout_launchpad = mm.get_output_port(self.var_lp_output.get())

    def callback_ext_output(self, *args):
        self.input_thread.midiout_external = mm.get_output_port(self.var_ext_output.get())

    def color_buttons(self):

        colors = mom.current_mode.background
        playfield = mom.current_mode.playfield

        for key_row, color_row, note_row in zip(self.all_keys, reversed(colors), reversed(playfield)):
            for key, color, note in zip(key_row, color_row, note_row): 
                actual_note = max(min(note + mom.current_mode.current_root_note, 127), -1)
                key['bg'] = maps.tk_color_codes[color]
                key['text'] = maps.midi_notes[actual_note]
                key['text'] = maps.midi_notes[actual_note]
    
    def highlight_button(self, note):
        row = 8 - int(note/10)
        column = note%10 -1
        
        self.all_keys[row][column]['bg'] = 'white'

    def release_button(self, note):
        row = 8 - int(note/10)
        column = note%10 -1

        colors = mom.current_mode.background
        
        self.all_keys[row][column]['bg'] = maps.tk_color_codes[colors[row][column]]

    def update_volume(self):
        self.var_volume_scale.set(ctrl.current_volume_pos)
        self.var_volume_scale_translated.set(maps.volume_positions[int(self.var_volume_scale.get())])

    def update_current_mode_name(self):
        self.label_current_mode_var['text'] = mom.current_mode.properties['name']

    def update_user_1_mode_name(self):
        if mom.favorites[0] is not None:
            self.label_user1_mode_var['text'] = mom.modes[mom.favorites[0]].properties['name']

        else:
            self.label_user1_mode_var['text'] = 'Not Set'

    def update_user_2_mode_name(self):
        if mom.favorites[1] is not None:
            self.label_user2_mode_var['text'] = mom.modes[mom.favorites[1]].properties['name']

        else:
            self.label_user2_mode_var['text'] = 'Not Set'

    def update_user_1_volume(self):
        if ctrl.favorites[0] is not None:
            self.label_user1_volume_var['text'] = maps.volume_positions[ctrl.favorites[0]]
        else:
            self.label_user1_volume_var['text'] = 'Not Set'

    def update_user_2_volume(self):
        if ctrl.favorites[1] is not None:
            self.label_user2_volume_var['text'] = maps.volume_positions[ctrl.favorites[1]]
        else:
            self.label_user2_volume_var['text'] = 'Not Set'

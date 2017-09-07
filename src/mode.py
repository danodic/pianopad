import pdb

import os.path

import translator as t
import map_manager as maps

class Mode:
    """
    A 'Mode' is pretty much a note mapping. You can have modes for different note mappings, like
    scales or anything fancy that comes to your mind.
    A mode is made from 3 files:
    . A file containing all the notes you want to map to
    . A file containing all the colors you want to assiciate to your notes
    . A file containing the properties of your mode
    The files must have the following names:
    - colors.txt
    - notes.txt
    - properties.txt
    They are txt files because we don't really want bullshit to edit them.
    They must be in a folder containing the mode name inside the "modes" folder in the {app} folder.
    This class will load the files from a given mode name folder and will store the data from the
    mode. It also contains the methods needed for triggering notes and etc.
    """

    # That has to be shared across all modes
    release_notes = {}

    def __init__(self, mode_folder_name):
        """

        """

        # Initialize the lists
        self.notes = None
        self.colors = None
        self.root_notes = None
        self.playfield = []
        self.background = []
        self.root_notes = []

        # Initialize the properties
        self.properties = {
            'name': None,
            'layout': None,
            'default': None,
            'octave size': None
        }

        # Check if we have the files neeedd
        self.validate_files(mode_folder_name)

        # Load the data
        self.parse_notes(mode_folder_name)
        self.parse_colors(mode_folder_name)
        self.parse_properties(mode_folder_name)
        
        # Make sure everything went fine
        self.validate_consistency()

        # Initialize status values
        self.current_root_note = 0
        self.current_row = int(self.properties['default row'])
        self.max_row = self.get_max_row()

        # Initialize the playfield
        self.refresh_playfield()

    def validate_files(self, mode_folder_name):
        """
        Will check if the files needed are present in the mode folder.
        """

        # Check if we have the folder and the files needed
        if not os.path.isdir(mode_folder_name):
            print("bad folder")
            # TODO trigger exception
            pass

        # Check if we have the files neeed
        for file in ['colors.txt', 'notes.txt', 'properties.txt']:
            if not os.path.isfile(mode_folder_name + os.sep + file):
                print("missing file")
                # TODO trigger exception
                pass

    def parse_notes(self, mode_folder_name):
        """
        Will load the notes file and store into a list.
        """

        # Load the notes file
        file_contents = open(mode_folder_name + os.sep + 'notes.txt').read()

        # Build the array
        file_array = file_contents.split('\n')

        # Initialize the notes array
        self.notes = []

        # Organizes the array
        for row in reversed(file_array):
            self.notes += row.split(",")

        # Convert everything to int
        self.notes = [int(c) for c in self.notes]

    def parse_colors(self, mode_folder_name):
        """
        Will load the colors file and store into a list.
        """

        # Load the notes file
        file_contents = open(mode_folder_name + os.sep + 'colors.txt').read()

        # Build the array
        file_array = file_contents.split('\n')

        # Initialize the notes array
        self.colors = []

        # Organizes the array
        for row in reversed(file_array):
            self.colors += row.split(",")

        # Convert everything to int
        self.colors = [int(c) for c in self.colors]

    def parse_properties(self, mode_folder_name):
        """
        Will parse the properties file.
        """

        # Load the notes file
        file_contents = open(mode_folder_name + os.sep + 'properties.txt').read()

        # Parse each option
        for row in file_contents.split("\n"):
            # TODO handle exception
            option_name, option_value = row.split(':')

            # Store the data
            if option_name.strip().lower() in ['name', 'layout', 'default row', 'octave size']:
                self.properties[option_name.strip().lower()] = option_value.strip()

    def validate_consistency(self):
        """
        Will make sure everything has been done properly after loading the files.
        It will just check if anything has remained as None after loading and parsing the files
        """

        if self.notes is None:
            #TODO handle exception
            pass

        if self.colors is None:
            #TODO handle exception
            pass

        for property_name in self.properties:
            if self.properties[property_name] is None:
                #TODO handle exception
                pass

        if len(self.notes) != len(self.colors):
            #TODO handle exception
            pass

    

    def move_down(self, increment=1):
        """
        TODO
        """

        if self.current_row > 0:
            self.current_row -= increment

        self.refresh_playfield()
    
    def move_up(self, increment=1):
        """
        TODO
        """
        if self.current_row < self.max_row :
            self.current_row += increment

        self.refresh_playfield()

    def get_max_row(self):
        note_amount = len(self.notes)
        column_size = maps.layouts[self.properties['layout']]
        row_amount = 8
        column_amount = 8/column_size

        return ( (note_amount / column_size) - (row_amount * column_amount) )  

    def root_note_up(self):
        """
        TODO
        """
        if self.current_root_note < 11:
            self.current_root_note += 1

        self.refresh_playfield()

    def root_note_down(self):
        """
        TODO
        """
        if self.current_root_note > 0:
            self.current_root_note -= 1

        self.refresh_playfield()

    def play_note(self, note, velocity, midiout_external, midiout_launchpad):
        """

        """

        # Get the note to be played
        actual_note = min(self.map_note_to_playfield(note) + self.current_root_note, 127)

        if actual_note < 0:
            return

        # Send the music note
        t.note_on(midiout_external, actual_note, velocity)

        # Send the light note
        t.light_on(midiout_launchpad, note, 63, 63, 63)

        # Add the note to the release queue
        if note not in self.release_notes:
            self.release_notes[note] = []

        if actual_note not in self.release_notes[note]:
            self.release_notes[note].append(actual_note)


    def release_note(self, note, midiout_external, midiout_launchpad):
        """

        """

        # Go thru each note and send the release note
        if note in self.release_notes:
            for to_release in self.release_notes[note]:
                t.note_off(midiout_external, to_release)

            # Release the light
            t.light_on_color_code(midiout_launchpad, note, self.map_note_to_colorfield(note))

    def refresh_playfield(self):

        # Reinitialize the playfield
        self.playfield = [None]*8
        self.background = [None]*8
        temp_root_notes = [None]*8

        # Reset the root notes
        self.refresh_root_notes()

        # Check what has to be done
        if self.properties['layout'] == '2 columns':
            
            # Build the playfield accordingly to the layout
            # Here we go reversed as the first notes are added to the bottom (end) of the array
            for row in reversed(range(8)):
                
                offset = self.current_row + row
                column_1 = offset * 4
                column_2 = (offset * 4) + 32

                #print(column_1, column_2)

                self.playfield[row] = self.notes[column_1:column_1+4] + self.notes[column_2:column_2+4]
                self.background[row] = self.colors[column_1:column_1+4] + self.colors[column_2:column_2+4]
                temp_root_notes[row] = self.root_notes[column_1:column_1+4] + self.root_notes[column_2:column_2+4]
        
        elif self.properties['layout'] == '1 column':

            for row in reversed(range(8)):
                
                offset = self.current_row + row
                offset = self.current_row + row
                column = offset * 8

                #print(column_1, column_2)

                self.playfield[row] = self.notes[column:column+8]
                self.background[row] = self.colors[column:column+8]
                temp_root_notes[row] = self.root_notes[column:column+8]

        # Merge the background and the root notes
        for row in range(8):
            for column in range(8):
                if temp_root_notes[row][column] != 0:
                    self.background[row][column] = 5

        #print(self.playfield)
    def map_note_to_playfield(self, note):

        # Define row and column
        row = int(note/10) - 1
        column = note % 10 - 1

        return self.playfield[row][column]

    def map_note_to_colorfield(self, note):

        # Define row and column
        row = int(note/10) - 1
        column = note % 10 - 1

        return self.background[row][column]

    def refresh_background(self, midiout):

        # Go over the screen array and draw it
        for row in range(8):
            for column in range(8):

                # Transform the coordinate into the proper note
                to_note = ((row+1) * 10) + (column+1)

                # Send the message
                t.light_on_color_code(midiout, to_note, self.background[row][column])
    
    def refresh_root_notes(self):

        # Intialize the note array
        self.root_notes = [0]*150

        # Find the first C
        note_count = len(self.notes)
        for i in range(note_count):
            note = self.notes[i]

            if note in maps.midi_notes:
                converted = maps.midi_notes[note]
                if 'C' in converted.strip().upper() and '#' not in converted.strip().upper():
                    first_c = i
                    break

        # fill the root notes
        for i in range((int( len(self.notes) / int(self.properties['octave size'] ))) + 2):
            self.root_notes[(int(self.properties['octave size'])*i+self.current_root_note) + first_c] = 1
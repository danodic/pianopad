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
        self.original_notes = None
        self.original_colors = None
        self.playfield_size = None
        self.colors = None
        self.playfield = []
        self.background = []
        self.root_notes = []

        # Initialize the properties
        self.properties = {
            'name': None,
            'layout': None,
            'default': None,
            'octave size': None,
            'root_notes': True
        }

        # Check if we have the files neeedd
        self.validate_files(mode_folder_name)

        # Load the data
        self.parse_notes(mode_folder_name)
        self.parse_colors(mode_folder_name)
        self.parse_properties(mode_folder_name)

        # Duplicate and store in the backups
        self.original_notes = list(self.notes)
        self.original_colors = list(self.colors)

        # Add the default padding
        #self.add_default_padding()

        # Get the default playfield size
        self.playfield_size = len(self.notes)
        
        # Make sure everything went fine
        self.validate_consistency()

        # Initialize status values
        self.current_root_note = 0
        self.padding = int(self.properties['padding'])
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
        file_contents = open(mode_folder_name + os.sep + 'notes.txt').readlines()

        # Initialize the notes array
        self.notes = []

        # Organizes the array
        for row in reversed(file_contents):
            self.notes += row.split(",")

        # Convert everything to int
        self.notes = [int(c) for c in self.notes]

    def parse_colors(self, mode_folder_name):
        """
        Will load the colors file and store into a list.
        """

        # Load the colors file
        file_contents = open(mode_folder_name + os.sep + 'colors.txt').readlines()

        # Initialize the notes array
        self.colors = []

        # Organizes the array
        for row in reversed(file_contents):
            self.colors += row.split(",")

        # Convert everything to int
        self.colors = [int(c) for c in self.colors]

    def parse_properties(self, mode_folder_name):
        """
        Will parse the properties file.
        """

        # Load the properties file
        file_contents = open(mode_folder_name + os.sep + 'properties.txt').readlines()

        # Parse each option
        for row in file_contents:
            # TODO handle exception
            option_name, option_value = row.split(':')
            option_name = option_name.strip().lower()

            # Store the data
            if option_name in ['name', 'layout', 'default row', 'octave size', 'padding']:
                self.properties[option_name] = option_value.strip()
            elif option_name == 'root_notes':
                if option_value.strip().lower() in ('no', 'false', '0'):
                    self.properties[option_name] = False
                elif option_value.strip().lower() in ('yes', 'true', '1'):
                    self.properties[option_name] = True
                else:
                    print('WARNING: unknown value for %s: %s' % (option_name, option_value))

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

        if self.current_row < self.get_max_row() :
            self.current_row += increment

        self.refresh_playfield()

    def slide_right(self, increment=1):
        if self.padding < maps.layouts[self.properties['layout']]:
            self.padding+=1

        self.refresh_playfield()

    def slide_left(self, increment=1):
        if self.padding > 0:
            self.padding-=1

        self.refresh_playfield()
    
    def get_max_row(self):
        note_amount = len(self.notes) + self.padding
        column_size = maps.layouts[self.properties['layout']]

        if self.properties['layout'] == '1 column':
            return (note_amount / column_size) - 8

        elif self.properties['layout'] == '2 columns':
            return (note_amount / column_size) - 16

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

    def play_note(self, note, velocity, midiout_external, launchpad):
        """

        """

        # Get the note to be played
        actual_note = min(self.map_note_to_playfield(note) + self.current_root_note, 127)

        if actual_note < 0:
            return

        # Send the music note
        t.note_on(midiout_external, actual_note, velocity)

        # Send the light note
        launchpad.light_on(note, 63, 63, 63)

        # Add the note to the release queue
        if note not in self.release_notes:
            self.release_notes[note] = []

        if actual_note not in self.release_notes[note]:
            self.release_notes[note].append(actual_note)


    def release_note(self, note, midiout_external, launchpad):
        """

        """

        # Go thru each note and send the release note
        if note in self.release_notes:
            for to_release in self.release_notes[note]:
                t.note_off(midiout_external, to_release)

            # Release the light
            launchpad.light_on_color_code(note, self.map_note_to_colorfield(note))

    def refresh_playfield(self):

        # Reinitialize the playfield
        self.playfield = [None]*8
        self.background = [None]*8

        # Get the initial position
        position = (self.current_row * maps.layouts[self.properties['layout']])

        #Add the amount of padding to the beginning of the notes
        use_notes = ([-1] * self.padding)
        use_colors = ([0] * self.padding)

        # Get the notes
        use_notes = use_notes + self.notes
        use_colors = use_colors + self.colors

        use_notes = use_notes[position:]
        use_colors = use_colors[position:]

        # In case we have more than 64 notes, truncate it.
        if len(use_notes) > 64:
            use_notes = use_notes[:64]

        # Else, add padding
        elif len(use_notes) < 64:
            use_notes = use_notes + ([-1] * (64 - len(use_notes)))

        # In case we have more than 64 notes, truncate it.
        if len(use_colors) > 64:
            use_colors = use_colors[:64]

        # Else, add padding
        elif len(use_colors) < 64:
            use_colors = use_colors + ([0] * (64 - len(use_colors)))

        # Reset the root notes
        if self.properties['root_notes']:
            self.refresh_root_notes(use_notes)

        if self.properties['layout'] == '2 columns':

            temp_playfield = [None]*16
            temp_background = [None]*16
            temp_root_notes = [None]*16

            for row in range(16):
                temp_playfield[row] = use_notes[(4*row):(4*row)+4]
                temp_background[row] = use_colors[(4*row):(4*row)+4]
                temp_root_notes[row] = self.root_notes[(4*row):(4*row)+4]

            for row in range(8):
                self.playfield[row] = temp_playfield[row] + temp_playfield[row+8]
                self.background[row] = temp_background[row] + temp_background[row+8]
                temp_root_notes[row] = temp_root_notes[row] + temp_root_notes[row+8]

        elif self.properties['layout'] == '1 column':

            temp_root_notes = [None]*8

            for row in range(8):
                self.playfield[row] = use_notes[(8*row):(8*row)+8]
                self.background[row] = use_colors[(8*row):(8*row)+8]
                temp_root_notes[row] = self.root_notes[(8*row):(8*row)+8]

        # Merge the background and the root notes
        if self.properties['root_notes']:
            for row in range(8):
                for column in range(8):
                    if temp_root_notes[row][column] != 0:
                        self.background[row][column] = 5

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

    def refresh_background(self, launchpad):

        # Go over the screen array and draw it
        for row in range(8):
            for column in range(8):

                # Transform the coordinate into the proper note
                to_note = ((row+1) * 10) + (column+1)

                # Send the message
                launchpad.light_on_color_code(to_note, self.background[row][column])
    
    def refresh_root_notes(self, notes):

        # Intialize some variables
        position = 0
        list_of_cs = [0,12,24,36,48,60,72,84,96,108,120]

        # Intialize the note array
        self.root_notes = [0] * len(notes)

        # Go over each position, add the root notes.
        # Ignore the padding
        while position < len(notes):

            if notes[position] in list_of_cs:
                self.root_notes[position] = 1

            # Move to the next position
            position +=1

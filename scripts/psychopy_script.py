from psychopy import visual, core, gui
import random
import nidaqmx
from nidaqmx.constants import LineGrouping

bit_value_dictionary = {
    'A': 1,
    'B': 2,
    'C': 3,
    'D': 4,
    'E': 5,
    'F': 6,
    'G': 7,
    'H': 8,
    'I': 9,
    'J': 10,
    'K': 11,
    'L': 12,
    'M': 13,
    'N': 14,
    'O': 15,
    'P': 16,
    'R': 17,
    'S': 18,
    'T': 19,
    'U': 20,
    'V': 21,
    'Z': 22,
    '0': 23,
}

def get_random_character(alphabet):
    if not alphabet:
        raise ValueError("The alphabet list is empty. No more characters to select.")

    # Select a random index from the remaining characters
    index = random.randint(0, len(alphabet) - 1)
    
    # Remove the character from the alphabet
    char = alphabet.pop(index)

    return char, index

def send_digital_output(input_char: str = 'A'):
    value = bit_value_dictionary.get(input_char, 0)

    print(f"Binary representation of '{input_char}': {value}")

    # Create a DAQmx task for digital output
    with nidaqmx.Task() as task:
        # Add a digital output channel for the 8 lines (port0/line0:7)
        task.do_channels.add_do_chan("myDAQ1/port0/line0:7", line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)

        # Write the binary value to the digital output lines
        task.write(value, auto_start=True)

        print("Digital output written to myDAQ.")

# Constants
alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
current_char_options = []

# Initialize the window
win = visual.Window(size=(800, 600), color="black", fullscr=False)

# Stimuli for display
letter_stim = visual.TextStim(win, text="", color="white", height=0.2, pos=(0, 0.2))

###                        ###
#    START OF THE EXPERIMENT #
###                        ###

# Get users input on what word does he want
dialog = gui.Dlg(title="Enter your word, with no spaces")
dialog.addField("Word:")
dialog.show()

wanted_word = ""
if dialog.OK:
    user_inputs = dialog.data
    wanted_word = user_inputs[0].upper()
    print(f"Wanted word is: {wanted_word}")
else:
    print("User canceled the dialog")
    core.quit()

for char in wanted_word.strip():
    current_char_options = alphabet.copy()

    # Display the start of the letter in word
    letter_stim.text = "NEXT: " + char
    letter_stim.draw()

    # Refresh the window
    win.flip()
    
    core.wait(2)

    # Sending start marker
    send_digital_output('0')

    core.wait(2)

    # Main loop
    while True:
        if len(current_char_options) <= 0:
            break
            
        current_char, current_char_index = get_random_character(current_char_options)

        # Display the current letter
        letter_stim.text = current_char
        letter_stim.draw()

        # Refresh the window
        win.flip()

        # Write the letter to EEG
        send_digital_output(current_char)
        
        # Wait for one second before another letter
        core.wait(1)

# Clean up
win.close()
core.quit()

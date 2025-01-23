from psychopy import visual, core
import random
import nidaqmx
from nidaqmx.constants import LineGrouping

letter_count = 0
response_list = list()
alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

def get_random_character(alphabet, response_list):
    if not alphabet:
        raise ValueError("The alphabet list is empty. No more characters to select.")

    # Select a random index from the remaining characters
    index = random.randint(0, len(alphabet) - 1)
    
    # Remove the character from the alphabet
    char = alphabet.pop(index)
    
    # Save char to the new list
    response_list.append(char)

    return char, index

def send_digital_output(input_char: str = 'A'):
    if input_char == '0':
        value = 0
    else:
        ascii_value = ord(input_char)
        value = ~ascii_value

    print(f"Binary representation of '{input_char}': {value}")

    # Create a DAQmx task for digital output
    with nidaqmx.Task() as task:
        # Add a digital output channel for the 8 lines (port0/line0:7)
        task.do_channels.add_do_chan("myDAQ1/port0/line0:7", line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)

        # Write the binary value to the digital output lines
        task.write(value, auto_start=True)

        print("Digital output written to myDAQ.")

# Initialize the window
win = visual.Window(color="black", fullscr=False)

# Stimuli for display
letter_stim = visual.TextStim(win, text="", color="white", height=0.2, pos=(0, 0.2))

# Timing control
clock = core.Clock()

# Main loop
while True:
    if len(alphabet) <= 0:
        break
        
    current_char, current_char_index = get_random_character(alphabet, response_list)

    # Display the current letter
    letter_stim.text = current_char
    letter_stim.draw()

    # Write the letter to EEG

    send_digital_output(current_char)
    
    # Wait for one second before another letter
    core.wait(1)

    # Refresh the window
    win.flip()

# Clean up
win.close()
core.quit()

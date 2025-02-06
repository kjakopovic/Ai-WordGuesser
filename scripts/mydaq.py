import nidaqmx
import time
from nidaqmx.constants import LineGrouping

from utils.marker_utils import convert_letter_to_marker

# Convert 'A' to 8-bit binary and send to myDAQ digital output
def send_digital_output(input_char: str = 'A'):
    value = convert_letter_to_marker(input_char)

    if value == -1:
        print(f"Invalid input character '{input_char}'.")
        return

    print(f"Binary representation of '{input_char}': {value}")

    # Create a DAQmx task for digital output
    with nidaqmx.Task() as task:
        # Add a digital output channel for the 8 lines (port0/line0:7)
        task.do_channels.add_do_chan("myDAQ1/port0/line0:7", line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)

        # Write the binary value to the digital output lines
        task.write(value, auto_start=True)

        print("Digital output written to myDAQ.")

# Execute the functions
send_digital_output()
time.sleep(1)
send_digital_output('0')

send_digital_output('B')
time.sleep(1)
send_digital_output('0')

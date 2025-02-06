import numpy as np
import logging
import mne
import os
import warnings

from utils import marker_utils

warnings.filterwarnings("ignore", category=RuntimeWarning)

logging.getLogger('mne').setLevel(logging.ERROR)
logging.getLogger('np').setLevel(logging.ERROR)

def get_letters_from_filepath(file_path: str):
    base_name = os.path.basename(file_path)
    
    file_name_without_extension = os.path.splitext(base_name)[0]
    
    letters = list(file_name_without_extension)
    
    return letters

def get_dataset_from_file(file_path: str):
    # List of letters to assign to each segment
    letters = get_letters_from_filepath(file_path)

    raw_data = mne.io.read_raw_brainvision(file_path, preload=True)

    # Apply bandpass filter
    raw_data.filter(0.1, 40, fir_design='firwin')

    # Extract events and event IDs
    events, event_id = mne.events_from_annotations(raw_data)

    # Convert event dictionary keys to integers
    first_key = next(iter(event_id))
    del event_id[first_key]

    # Check if marker 23 exists
    if 'Stimulus/S 23' not in event_id:
        print("Marker 23 not found in event data.")
        return None

    # Get the indices where 'Stimulus/S 23' events occur
    stimulus_23_indices = events[:, -1] == event_id['Stimulus/S 23']

    # Extract the indices of the 'Stimulus/S 23' events
    stimulus_23_event_positions = events[stimulus_23_indices]

    # We'll create a list of events between each pair of 'Stimulus/S 23' markers
    all_events_between_23 = []

    # Loop through the 'Stimulus/S 23' events to select the events in between
    for i in range(1, len(stimulus_23_event_positions)):
        # Get the start and end indices of the events between two 'Stimulus/S 23' events
        start_idx = stimulus_23_event_positions[i - 1, 0]  # The first event
        end_idx = stimulus_23_event_positions[i, 0]  # The next event

        # Filter the events that are between the two 'Stimulus/S 23' events
        events_between = events[(events[:, 0] > start_idx) & (events[:, 0] < end_idx)]

        # Add the filtered events to the list
        all_events_between_23.extend(events_between)

    # Create epochs using the filtered events (events between 'Stimulus/S 23')
    epochs_between_23 = mne.Epochs(
        raw_data, np.array(all_events_between_23), event_id=None,
        tmin=-0.1, tmax=0.8, baseline=(None, 0),
        preload=True
    )

    # Get the EEG data as a NumPy array (samples x channels x time)
    X = epochs_between_23.get_data()

    # Get the markers associated with each event
    markers = epochs_between_23.events[:, -1]

    data_with_markers_and_letters = []

    # We will keep track of which segment we are in
    segment_idx = 0
    current_letter = letters[segment_idx]

    # Loop through the extracted epochs and assign the letter based on the segment
    for i, (epoch_data, marker) in enumerate(zip(X, markers)):
        # If we have exhausted the current segment, move to the next letter
        if i > 0 and events[i, 0] == stimulus_23_event_positions[segment_idx, 0]:
            segment_idx += 1
            current_letter = letters[segment_idx % len(letters)]

        # Append the epoch data, marker, and corresponding letter
        data_with_markers_and_letters.append([epoch_data, marker, marker_utils.convert_letter_to_marker(current_letter.upper())])

    # Return the data with markers and letters
    return data_with_markers_and_letters

def iterate_and_process_ahdr_files(directory: str):
    # List all files in the specified directory
    files = os.listdir(directory)
    dataset = []

    # Filter out only the .ahdr files
    ahdr_files = [file for file in files if file.endswith('.ahdr') and 'copy' not in file.lower()]

    for ahdr_file in ahdr_files:
        file_path = os.path.join(directory, ahdr_file)
        print(f"Processing file: {file_path}")
        
        current_dataset = get_dataset_from_file(file_path)
        dataset.extend(current_dataset)

    return dataset

def process_eeg_data(data):
    X = []
    y = []
    
    for entry in data:
        eeg_data = entry[0]  # shape: (n_epochs, n_channels, n_samples)
        label1 = entry[1]    # First label
        label2 = entry[2]    # Second label, used as target variable y

        eeg_data = eeg_data.reshape(eeg_data.shape[0], 1, eeg_data.shape[1])
        label1_array = np.full((eeg_data.shape[0], 1, eeg_data.shape[2]), label1)

        # Concatenate label1 as an extra channel
        eeg_data_with_label = np.concatenate((eeg_data, label1_array), axis=1)  # New shape: (n_epochs, n_channels + 1, n_samples)

        # Append to lists
        X.append(eeg_data_with_label)
        y.append(label2)
    
    # Convert lists to NumPy arrays for further processing
    X = np.array(X)
    y = np.array(y)
    
    return X, y
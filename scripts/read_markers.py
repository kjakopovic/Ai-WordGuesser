import mne

file_path = '../../../../Vision/Raw Files/VAMP-2-000011.ahdr'
file_path_amrk = '../../../../Vision/Raw Files/VAMP-2-000011.amrk'

# AHDR FILE READINGS
raw_data = mne.io.read_raw_brainvision(file_path, preload=True)

# Print info about the EEG data
print(raw_data.info)

events, event_id = mne.events_from_annotations(raw_data)

# Display the events
print("Events found in the data:")
print(events)

# Unique event types
print("Unique event IDs (markers):")
print(event_id)

# AMRK FILE READINGS
# def read_amrk_file(file_path):
#     markers = []
#     with open(file_path, 'r') as file:
#         for line in file:
#             marker = line.strip().split(", ")
#             markers.append(marker)
#     return markers

# # Example usage
# markers = read_amrk_file(file_path_amrk)
# for marker in markers:
#     print(f"Marker: {marker}")

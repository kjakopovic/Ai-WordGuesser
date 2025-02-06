import mne
import numpy as np

bit_value_dictionary = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 
    'I': 9, 'J': 10, 'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 
    'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'Z': 22, '0': 23
}

def convert_marker_to_letter(marker: str):
    if "New Segment" in marker:
        return None
    marker = marker.split("/")[1][1:]
    reverse_dict = {v: k for k, v in bit_value_dictionary.items()}
    return reverse_dict.get(int(marker), None)

def calculate_band_power(epoch_data, sfreq, fmin, fmax):
    fft_result = np.fft.rfft(epoch_data)
    freqs = np.fft.rfftfreq(len(epoch_data), d=1./sfreq)
    return np.sum(np.abs(fft_result[(freqs >= fmin) & (freqs <= fmax)]) ** 2)

file_path = '../data/app.ahdr'
raw_data = mne.io.read_raw_brainvision(file_path, preload=True)

events, event_id = mne.events_from_annotations(raw_data)

epochs = mne.Epochs(
    raw_data, events, event_id=event_id, tmin=-0.2, tmax=0.5, baseline=(None, 0), preload=True
)

all_channels = epochs.info['ch_names']

segments = []
current_segment = {}

for event_id_key, epoch_data in zip(event_id.keys(), epochs):
    marker_name = convert_marker_to_letter(event_id_key)
    if marker_name is None:
        continue
    
    if marker_name == '0':  # Separation marker
        if current_segment:
            segments.append(current_segment)
            current_segment = {}
        continue
    
    total_powers = []
    for channel in all_channels:
        ch_data = epoch_data[epochs.info['ch_names'].index(channel)]
        total_power = np.sum(np.abs(np.fft.rfft(ch_data)) ** 2)
        total_powers.append(total_power)
    
    avg_total_power = np.mean(total_powers)
    current_segment[marker_name] = avg_total_power

if current_segment:
    segments.append(current_segment)

print("Most Intense Marker in Each Segment:")
for i, segment in enumerate(segments):
    if segment:
        strongest_marker = max(segment, key=segment.get)
        print(f"Segment {i + 1}: {strongest_marker} with Power {segment[strongest_marker]:.5f}")

import mne
import numpy as np
from scipy.signal import find_peaks

# TODO: na pocetku traziti da upise rijec koju trazi i onda odraditi mjerenja za tu rijec (splitat rijeci sa markerima za start i kraj tipa 0b11111111)
# TODO: napraviti CNN za klasifikaciju (nml, eegnet sluze za klasifikaciju eegova)

def convert_marker_to_letter(marker: str):
    if "New Segment" in marker:
        return
    
    marker = marker.split("/")[1]
    marker = marker[1:]

    ascii_value = int(marker) & 0b11111111
    ascii_value = ~ascii_value
    ascii_value = chr(256 + ascii_value)
    
    return ascii_value
    
def calculate_dominant_frequency_power(epoch_data, sfreq):
    # Apply FFT to the epoch data
    fft_result = np.fft.rfft(epoch_data)
    freqs = np.fft.rfftfreq(len(epoch_data), d=1./sfreq)
    
    # Find the peak in the FFT result
    peak_indices, _ = find_peaks(np.abs(fft_result))
    
    if peak_indices.size > 0:
        # Get the frequency and the power of the strongest peak
        dominant_index = peak_indices[np.argmax(np.abs(fft_result[peak_indices]))]
        dominant_freq = freqs[dominant_index]
        dominant_power = np.abs(fft_result[dominant_index]) ** 2
    else:
        dominant_freq = 0
        dominant_power = 0
    
    return dominant_freq, dominant_power

def calculate_band_power(epoch_data, sfreq, fmin, fmax):
    fft_result = np.fft.rfft(epoch_data)
    freqs = np.fft.rfftfreq(len(epoch_data), d=1./sfreq)
    band_power = np.sum(np.abs(fft_result[(freqs >= fmin) & (freqs <= fmax)]) ** 2)
    return band_power

# File paths
file_path = '../../../../Vision/Raw Files/VAMP-2-000011.ahdr'

# Load the raw data
raw_data = mne.io.read_raw_brainvision(file_path, preload=True)

# Filtering fequencies
raw_data.filter(25, 44, fir_design='firwin')

# Extract events and event IDs
events, event_id = mne.events_from_annotations(raw_data)

# Create epochs around each event
epochs = mne.Epochs(
    raw_data, 
    events, 
    event_id=event_id, 
    tmin=-0.2, 
    tmax=0.5, 
    baseline=(None, 0),
    preload=True
)

marker_channel_powers = {}

for event_id_key, epoch_data in zip(event_id.keys(), epochs):
    # Get the data for Fz and Cz channels
    fz_data = epoch_data[epochs.info['ch_names'].index('Fz')]  # Extract Fz channel data
    cz_data = epoch_data[epochs.info['ch_names'].index('Cz')]  # Extract Cz channel data
    
    # Calculate total power and alpha band power for Fz
    fz_total_power = np.sum(np.abs(np.fft.rfft(fz_data)) ** 2)
    fz_alpha_power = calculate_band_power(fz_data, epochs.info['sfreq'], 8, 12)
    
    # Calculate total power and alpha band power for Cz
    cz_total_power = np.sum(np.abs(np.fft.rfft(cz_data)) ** 2)
    cz_alpha_power = calculate_band_power(cz_data, epochs.info['sfreq'], 8, 12)
    
    # Calculate averages of total power and alpha power between Fz and Cz
    avg_total_power = (fz_total_power + cz_total_power) / 2
    avg_alpha_power = (fz_alpha_power + cz_alpha_power) / 2

    # Convert the marker to a readable format
    marker_name = convert_marker_to_letter(event_id_key)
    
    # Store the powers for Fz and Cz
    if marker_name:
        marker_channel_powers[marker_name] = {
            'Fz': {'total_power': fz_total_power, 'alpha_power': fz_alpha_power},
            'Cz': {'total_power': cz_total_power, 'alpha_power': cz_alpha_power},
            'Avg': {'total_power': avg_total_power, 'alpha_power': avg_alpha_power}
        }

# Find the most intense marker for each channel
fz_most_intense_marker = max(marker_channel_powers, key=lambda k: marker_channel_powers[k]['Fz']['total_power'])
cz_most_intense_marker = max(marker_channel_powers, key=lambda k: marker_channel_powers[k]['Cz']['total_power'])
avg_most_intense_marker = max(marker_channel_powers, key=lambda k: marker_channel_powers[k]['Avg']['total_power'])

# Print the results
print("Results by Marker and Channel:")
for marker, powers in marker_channel_powers.items():
    print(f"Marker: {marker}")
    print(f"  Fz - Total Power: {powers['Fz']['total_power']:.5f}, Alpha Power: {powers['Fz']['alpha_power']:.5f}")
    print(f"  Cz - Total Power: {powers['Cz']['total_power']:.5f}, Alpha Power: {powers['Cz']['alpha_power']:.5f}")
    print(f"  Avg - Total Power: {powers['Avg']['total_power']:.5f}, Alpha Power: {powers['Avg']['alpha_power']:.5f}")

print("\nMost Intense Stimulus by Channel:")
print(f"Fz - Most Intense Marker: {fz_most_intense_marker}, Total Power: {marker_channel_powers[fz_most_intense_marker]['Fz']['total_power']:.5f}")
print(f"Cz - Most Intense Marker: {cz_most_intense_marker}, Total Power: {marker_channel_powers[cz_most_intense_marker]['Cz']['total_power']:.5f}")
print(f"Avg - Most Intense Marker: {avg_most_intense_marker}, Total Power: {marker_channel_powers[avg_most_intense_marker]['Avg']['total_power']:.5f}")
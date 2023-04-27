import mido
import numpy as np

def normalize_velocities(midi_data, target_range=(40, 100)):
    velocities = []

    # Collect all velocities from the MIDI data
    for track in midi_data.tracks:
        for msg in track:
            if msg.type == 'note_on' and msg.velocity > 0:
                velocities.append(msg.velocity)

    if not velocities:
        return midi_data

    # Calculate mean and standard deviation of velocities
    mean_velocity = np.mean(velocities)
    std_velocity = np.std(velocities)

    # Rescale velocities
    for track in midi_data.tracks:
        for msg in track:
            if msg.type == 'note_on' and msg.velocity > 0:
                normalized_velocity = (msg.velocity - mean_velocity) / std_velocity
                rescaled_velocity = int(np.clip(normalized_velocity * (target_range[1] - target_range[0]) / 2 + np.mean(target_range), 1, 127))
                msg.velocity = rescaled_velocity

    return midi_data

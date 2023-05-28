import numpy as np
from sklearn.model_selection import train_test_split

def split_train_validation_data(preprocessed_midi_data, validation_ratio=0.2):
    train_data, validation_data = train_test_split(preprocessed_midi_data, test_size=validation_ratio, random_state=42)
    return train_data, validation_data


def preprocess_data_for_training(preprocessed_midi_data, label, sequence_length=32):
    sequences = []
    labels = []

    for midi_file_data in preprocessed_midi_data:
        midi_events = []

        # Extract MIDI events from the MidiFile object
        for track in midi_file_data.tracks:
            for event in track:
                midi_events.append(event)

        for i in range(len(midi_events) - sequence_length):
            sequence = midi_events[i:i+sequence_length]
            sequence_features = []
            for event in sequence:
                if hasattr(event, 'note'):
                    sequence_features.append([event.note, event.time])
                else:
                    sequence_features.append([0, event.time])  # Replace with appropriate handling

            sequences.append(sequence_features)
            labels.append(label)

    # Convert to numpy arrays and ensure they are 2D
    sequences = np.array(sequences)
    if sequences.ndim < 2:
        sequences = np.expand_dims(sequences, axis=-1)
    labels = np.array(labels)

    return sequences, labels

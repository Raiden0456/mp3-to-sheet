import numpy as np
from sklearn.model_selection import train_test_split

def split_train_validation_data(preprocessed_midi_data, validation_ratio=0.2):
    train_data, validation_data = train_test_split(preprocessed_midi_data, test_size=validation_ratio, random_state=42)
    return train_data, validation_data

def preprocess_data_for_training(preprocessed_midi_data, sequence_length=32):
    sequences = []
    labels = []
    print("Type of preprocessed_midi_data: ", type(preprocessed_midi_data))

    for midi_file_data in preprocessed_midi_data:
        midi_events = []

        # Extract MIDI events from the MidiFile object
        for track in midi_file_data.tracks:
            for event in track:
                midi_events.append(event)

        for i in range(len(midi_events) - sequence_length):
            sequence = midi_events[i:i+sequence_length]
            label = midi_events[i+sequence_length]

            # Adjust how you extract features from MIDI events
            sequence_features = np.array([[event.note, event.time] for event in sequence])
            label_encoded = label.note

            sequences.append(sequence_features)
            labels.append(label_encoded)

    return np.array(sequences), np.array(labels)
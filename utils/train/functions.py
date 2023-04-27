import numpy as np
from sklearn.model_selection import train_test_split

def split_train_validation_data(preprocessed_midi_data, validation_ratio=0.2):
    train_data, validation_data = train_test_split(preprocessed_midi_data, test_size=validation_ratio, random_state=42)
    return train_data, validation_data

def preprocess_data_for_training(preprocessed_midi_data, sequence_length=32):
    sequences = []
    labels = []

    for midi_file_data in preprocessed_midi_data:
        for i in range(len(midi_file_data) - sequence_length):
            sequence = midi_file_data[i:i+sequence_length]
            label = midi_file_data[i+sequence_length]
            
            # Here need to adjust how we're extracting features from your MIDI data
            sequence_features = np.array([[event.note, event.time] for event in sequence])
            label_encoded = label.note 

            sequences.append(sequence_features)
            labels.append(label_encoded)

    return np.array(sequences), np.array(labels)
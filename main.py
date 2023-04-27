import os
import mido
import tensorflow as tf
from utils.preprocess.quantize_note_timings import quantize_note_timings
from utils.preprocess.normalize_velocities import normalize_velocities
from utils.preprocess.filter_unnecessary_data import filter_unnecessary_data
from utils.train.functions import split_train_validation_data, preprocess_data_for_training
from music21 import *

# Read and parse MIDI file using mido
def parse_midi_file(midi_file_path):
    midi_data = mido.MidiFile(midi_file_path)
    return midi_data

# Preprocess MIDI data before feeding it to the machine learning model
def preprocess_midi_data(midi_data):
    midi_data = quantize_note_timings(midi_data)
    midi_data = normalize_velocities(midi_data)
    midi_data = filter_unnecessary_data(midi_data)
    pass

# Load a list of MIDI files for training and validation
def load_midi_files(file_directory):
    midi_files = []
    for file in os.listdir(file_directory):
        if file.endswith(".mid") or file.endswith(".midi"):
            midi_files.append(os.path.join(file_directory, file))
    return midi_files

def train_lstm_model(train_sequences, train_labels, validation_sequences, validation_labels, input_shape, num_classes):
    # Define the LSTM model architecture
    model = tf.keras.Sequential([
        tf.keras.layers.InputLayer(input_shape=input_shape),
        tf.keras.layers.LSTM(units=128, return_sequences=True),
        tf.keras.layers.LSTM(units=128),
        tf.keras.layers.Dense(units=num_classes, activation='softmax')
    ])

    # Compile the model
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # Fit the model to the data
    history = model.fit(train_sequences, train_labels, epochs=20, validation_data=(validation_sequences, validation_labels))

    return model, history

def train_machine_learning_model():
    # Load and preprocess my MIDI data
    file_directory = "path/to/my/midi/files"
    midi_files = load_midi_files(file_directory)
    preprocessed_midi_data = [preprocess_midi_data(parse_midi_file(file)) for file in midi_files]

    # Split the preprocessed MIDI data into training and validation sets
    train_data, validation_data = split_train_validation_data(preprocessed_midi_data)

    # Further preprocess the MIDI data to create input sequences and corresponding labels for training
    train_sequences, train_labels = preprocess_data_for_training(train_data)
    validation_sequences, validation_labels = preprocess_data_for_training(validation_data)

    # Determine input_shape and num_classes based on preprocessed data
    input_shape = (sequence_length, num_features)
    num_classes = num_classes_based_on_data

    # Train the LSTM model
    model, history = train_lstm_model(train_sequences, train_labels, validation_sequences, validation_labels, input_shape, num_classes)

    return model, history


def filter_midi_data(midi_data, model):
    # Use the trained machine learning model to filter MIDI data
    pass

def convert_midi_to_music_representation(midi_data):
    # Convert MIDI data to music representation using music21
    pass

def generate_sheet_music(music_representation):
    # Generate sheet music using music21
    pass

def export_sheet_music(sheet_music, output_format):
    # Export sheet music to desired format (e.g., PDF)
    pass

if __name__ == "__main__":
    midi_file_path = "path/to/your/midi/file.mid"
    midi_data = parse_midi_file(midi_file_path)
    preprocess_midi_data(midi_data)

    model = train_machine_learning_model()
    filter_midi_data(midi_data, model)

    music_representation = convert_midi_to_music_representation(midi_data)
    sheet_music = generate_sheet_music(music_representation)
    export_sheet_music(sheet_music, "pdf")

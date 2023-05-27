import os
import mido
import tensorflow as tf
import tkinter as tk
from tkinter import filedialog
import numpy as np
from utils.preprocess.quantize_note_timings import quantize_note_timings
from utils.preprocess.normalize_velocities import normalize_velocities
from utils.preprocess.filter_unnecessary_data import filter_unnecessary_data
from utils.train.functions import split_train_validation_data, preprocess_data_for_training
from music21 import *
import musescore

# Read and parse MIDI file using mido
def parse_midi_file(midi_file_path):
    midi_data = mido.MidiFile(midi_file_path)
    return midi_data

# Preprocess MIDI data before feeding it to the machine learning model
def preprocess_midi_data(midi_data):
    midi_data = quantize_note_timings(midi_data)
    midi_data = normalize_velocities(midi_data)
    midi_data = filter_unnecessary_data(midi_data)
    return midi_data

# Load a list of MIDI files for training and validation
def load_midi_files(file_directory):
    midi_files = []
    for root, dirs, files in os.walk(file_directory):
        for file in files:
            if file.endswith(".mid") or file.endswith(".midi"):
                midi_files.append(os.path.join(root, file))

    return midi_files

def train_lstm_model(train_sequences, train_labels, validation_sequences, validation_labels, input_shape, num_classes):

    print("Train sequences shape: ", train_sequences.shape)
    print("Train labels shape: ", train_labels.shape)
    print("Validation sequences shape: ", validation_sequences.shape)
    print("Validation labels shape: ", validation_labels.shape)
    print("Input shape: ", input_shape)
    print("Number of classes: ", num_classes)

    # Define the LSTM model architecture
    model = tf.keras.Sequential([
        tf.keras.layers.InputLayer(input_shape=input_shape),
        tf.keras.layers.LSTM(units=128, return_sequences=True),
        tf.keras.layers.LSTM(units=128),
        tf.keras.layers.Dense(units=num_classes, activation='softmax')
    ])

    print(model.summary())
    print("Model input shape: ", model.input_shape)
    print("Model output shape: ", model.output_shape)
    

    # Compile the model
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # Fit the model to the data
    history = model.fit(train_sequences, train_labels, epochs=20, validation_data=(validation_sequences, validation_labels))

    return model, history

def train_machine_learning_model():
    # Load and preprocess my MIDI data
    file_directory = "./adl-piano-midi/Children"
    midi_files = load_midi_files(file_directory)
    print("Loaded {} MIDI files".format(len(midi_files)))

    preprocessed_midi_data = [preprocess_midi_data(parse_midi_file(file)) for file in midi_files]
    print("Preprocessed {} MIDI files".format(len(preprocessed_midi_data)))

    # Split the preprocessed MIDI data into training and validation sets
    train_data, validation_data = split_train_validation_data(preprocessed_midi_data)
    print("Split {} MIDI files into {} training files and {} validation files".format(len(preprocessed_midi_data), len(train_data), len(validation_data)))

    # Further preprocess the MIDI data to create input sequences and corresponding labels for training
    train_sequences, train_labels = preprocess_data_for_training(train_data)
    print("Created {} training sequences and {} training labels".format(len(train_sequences), len(train_labels)))

    validation_sequences, validation_labels = preprocess_data_for_training(validation_data)
    print("Created {} validation sequences and {} validation labels".format(len(validation_sequences), len(validation_labels)))

    # Determine input_shape and num_classes based on preprocessed data
    input_shape = train_sequences.shape[1:] # Use the shape of the sequences for input_shape
    num_classes = np.max(train_labels) + 1 # Determine the number of unique classes in train_labels

    # Train the LSTM model
    model, history = train_lstm_model(train_sequences, train_labels, validation_sequences, validation_labels, input_shape, num_classes)
    return model, history

def filter_midi_data(midi_data, model):
    print("Midi data type: ", type(midi_data))
    # Convert the MIDI data to numerical format suitable for the model
    preprocessed_data = preprocess_midi_data(midi_data)

    # Perform the prediction using the preprocessed data
    predictions = model.predict(preprocessed_data)
    return predictions

def convert_midi_to_music_representation(midi_data):
    # Convert MIDI data to music representation using music21
    music_rep = converter.parse(midi_data)
    return music_rep

def generate_sheet_music(music_representation):
    sheet_music = music_representation
    return sheet_music

def export_sheet_music(sheet_music, output_format, filename):
    # Export sheet music to desired format (e.g., PDF)
    sheet_music.write(output_format, fp=filename)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # we don't want a full GUI, so keep the root window from appearing
    midi_file_path = filedialog.askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    midi_data = parse_midi_file(midi_file_path)
    preprocess_midi_data(midi_data)
    model = train_machine_learning_model()
    filter_midi_data(midi_data, model[0])

    music_representation = convert_midi_to_music_representation(midi_file_path)
    sheet_music = generate_sheet_music(music_representation)
    output_file_path_XML = "./resultXML/" + os.path.splitext(os.path.basename(midi_file_path))[0] + ".xml"
    output_file_path_PDF = "./resultPDF/" + os.path.splitext(os.path.basename(midi_file_path))[0] + ".pdf"
    export_sheet_music(sheet_music, "musicxml", output_file_path_XML)
    

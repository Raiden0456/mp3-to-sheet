import numpy as np
import mido
# Preprocess MIDI data for prediction
def preprocess_data_for_prediction(midi_data, sequence_length=32):
    midi_events = []
    # Extract MIDI events from the MidiFile object
    for track in midi_data.tracks:
        for event in track:
            midi_events.append(event)
    sequences = []
    for i in range(len(midi_events) - sequence_length):
        sequence = midi_events[i:i+sequence_length]
        # Adjust how to extract features from MIDI events
        sequence_features = []
        for event in sequence:
            if hasattr(event, 'note'):
                sequence_features.append([event.note, event.time])
            else:
                sequence_features.append([0, event.time]) # Replace with appropriate handling
        sequences.append(sequence_features)
    return np.array(sequences)

# Postprocess predicted sequences to MIDI data
def postprocess_sequences_to_midi(sequence, output_file_path):
    # Create a new MIDI file
    midi = mido.MidiFile()

    # Create a new track
    track = mido.MidiTrack()
    midi.tracks.append(track)

    # Convert each note in the sequence to a MIDI message and add it to the track
    for note in sequence:
        # Create a new note_on message and add it to the track
        note_on = mido.Message('note_on', note=note, velocity=64, time=0)
        track.append(note_on)

        # Create a new note_off message and add it to the track
        note_off = mido.Message('note_off', note=note, velocity=64, time=480)
        track.append(note_off)

    # Save the MIDI file
    midi.save(output_file_path)

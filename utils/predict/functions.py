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
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)

    for note_sequence in sequence:
        for note in note_sequence:
            # Ensure the note value is an integer
            note = int(note)

            note_on = mido.Message('note_on', note=note, velocity=64, time=0)
            track.append(note_on)

            note_off = mido.Message('note_off', note=note, velocity=64, time=960)
            track.append(note_off)

    mid.save(output_file_path)



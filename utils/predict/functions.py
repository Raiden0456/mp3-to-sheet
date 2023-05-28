import numpy as np
import mido
# Preprocess MIDI data for prediction
def preprocess_data_for_prediction(midi_data, sequence_length=32):
    midi_events = []
    # Extract MIDI events from the MidiFile object
    for track in midi_data.tracks:
        for event in track:
            if hasattr(event, 'note'):
                midi_events.append([event.note, event.time])
            else:
                midi_events.append([0, event.time]) # Replace with appropriate handling

    sequences = []
    for i in range(len(midi_events) - sequence_length):
        sequence = midi_events[i:i+sequence_length]
        sequences.append(sequence)

    return np.array(sequences)

# Postprocess predicted sequences to MIDI data
def postprocess_predictions_to_midi(predictions, midi_data, threshold=0.5, output_file_path="output.mid"):
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)

    for i, track in enumerate(midi_data.tracks):
        for event in track:
            if hasattr(event, 'note'):
                # If the model predicts the note is pure, include it in the new MIDI file
                if predictions[i] >= threshold:
                    track.append(event)

    mid.save(output_file_path)
    return mid



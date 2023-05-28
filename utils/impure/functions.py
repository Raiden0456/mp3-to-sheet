import mido
import random
import os
from mido.midifiles.meta import KeySignatureError

def make_midi_impure(midi_file_path, alteration_probability=0.1):
    try:
        # Load the MIDI file
        midi = mido.MidiFile(midi_file_path)

        # Variable to keep track of altered note
        altered_note = None

        # Iterate over all notes in all tracks
        for track in midi.tracks:
            for msg in track:
                if msg.type == 'note_on':
                    # With a certain probability, alter the note
                    if random.random() < alteration_probability:
                        altered_note = random.randint(0, 127)
                        msg.note = altered_note
                    else:
                        altered_note = None
                elif msg.type == 'note_off' and altered_note is not None:
                    # If this is a note_off event for a note that was altered, alter it to match
                    msg.note = altered_note

        # Save the altered MIDI file to adl-piano-midi/impure with the same filepath
        midi_file_name = os.path.basename(midi_file_path)
        midi_file_name = midi_file_name.replace('.mid', '_impure.mid')
        midi_file_name = midi_file_name.replace('.midi', '_impure.mid')
        
        # Preserve the subdirectory structure
        subdirectory = os.path.dirname(midi_file_path).replace('adl-piano-midi', '')
        output_directory = os.path.join('adl-piano-midi-impure', subdirectory)
        os.makedirs(output_directory, exist_ok=True)
        
        output_file_path = os.path.join(output_directory, midi_file_name)
        midi.save(output_file_path)
    except (KeySignatureError, EOFError, OSError) as e:
        print(f"Skipping file {midi_file_path} due to {type(e).__name__}: {e}")
        # Delete the corrupted file from the original directory
        os.remove(midi_file_path)


def process_directory(directory_path):
    # Iterate over all files in the directory and its subdirectories
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            # If the file is a MIDI file, make it impure
            if file.endswith('.mid') or file.endswith('.midi'):
                midi_file_path = os.path.join(root, file)
                make_midi_impure(midi_file_path)

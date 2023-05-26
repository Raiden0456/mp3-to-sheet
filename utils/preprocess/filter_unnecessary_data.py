import mido

def filter_unnecessary_data(midi_data):
    filtered_tracks = []
    all_msgs = []
    filtered_msgs = []

    for track in midi_data.tracks:
        filtered_track = mido.MidiTrack()
        note_on_events = set()

        for msg in track:
            all_msgs.append(msg)  # Record all messages
            if msg.type == 'note_on' and msg.velocity > 0:
                note_on_events.add((msg.note, msg.channel))
                filtered_track.append(msg)
                filtered_msgs.append(msg)  # Record filtered messages

            elif (msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0)) and (msg.note, msg.channel) in note_on_events:
                note_on_events.remove((msg.note, msg.channel))
                filtered_track.append(msg)
                filtered_msgs.append(msg)  # Record filtered messages

            elif msg.type == 'set_tempo' or msg.type == 'time_signature':
                filtered_track.append(msg)
                filtered_msgs.append(msg)  # Record filtered messages

        filtered_tracks.append(filtered_track)

    filtered_midi_data = mido.MidiFile()
    filtered_midi_data.ticks_per_beat = midi_data.ticks_per_beat
    filtered_midi_data.tracks = filtered_tracks

    # Compute the messages that were removed
    # removed_msgs = [msg for msg in all_msgs if msg not in filtered_msgs]

    # Now print or otherwise removed messages
    # for msg in removed_msgs:
    #     print("change:", msg)

    return filtered_midi_data


def quantize_note_timings(midi_data, quantize_to=16, mode="both"):
    ticks_per_quantize = midi_data.ticks_per_beat // quantize_to
    start_times = []
    durations = []

    for track in midi_data.tracks:
        current_time = 0
        for msg in track:
            current_time += msg.time

            if msg.type == 'note_on' and msg.velocity > 0:
                start_times.append((msg, current_time))

            if (msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0)):
                start_times, duration = find_matching_note_on(msg, start_times)
                if duration:
                    durations.append((msg, duration))

    if mode in ["start_times", "both"]:
        start_times = quantize_times(start_times, ticks_per_quantize)
    if mode in ["durations", "both"]:
        durations = quantize_times(durations, ticks_per_quantize)

    return reconstruct_midi_data(midi_data, start_times, durations)

def find_matching_note_on(note_off_msg, start_times):
    for i, (note_on_msg, start_time) in enumerate(start_times):
        if note_on_msg.note == note_off_msg.note and note_on_msg.channel == note_off_msg.channel:
            duration = note_off_msg.time - start_time
            del start_times[i]
            return start_times, duration
    return start_times, None

def quantize_times(times_list, ticks_per_quantize):
    return [(msg, round(time / ticks_per_quantize) * ticks_per_quantize) for msg, time in times_list]

def reconstruct_midi_data(midi_data, start_times, durations):
    start_times_dict = {msg: time for msg, time in start_times}
    durations_dict = {msg: duration for msg, duration in durations}

    for track in midi_data.tracks:
        current_time = 0
        for msg in track:
            current_time += msg.time

            if msg.type == 'note_on' and msg.velocity > 0 and msg in start_times_dict:
                msg.time = start_times_dict[msg] - current_time

            if (msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0)) and msg in durations_dict:
                matching_note_on, _ = find_matching_note_on(msg, start_times)
                if matching_note_on:
                    msg.time = start_times_dict[matching_note_on] + durations_dict[msg] - current_time

    return midi_data

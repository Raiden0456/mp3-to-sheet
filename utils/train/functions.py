from sklearn.model_selection import train_test_split

def split_train_validation_data(preprocessed_midi_data, validation_ratio=0.2):
    train_data, validation_data = train_test_split(preprocessed_midi_data, test_size=validation_ratio, random_state=42)
    return train_data, validation_data


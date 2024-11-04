import os

from pydub import AudioSegment


class AudioData:
    def __init__(self, audio_path, serial_number, event):
        self.audio_path = audio_path
        self.serial_number = serial_number
        self.event = event

    def load_data(self):
        # Placeholder to load or prepare audio data if needed
        pass

    def set_serial_number(self, new_serial):
        self.serial_number = new_serial

    def create_split(self, split_path, split_serial):
        return AudioData(audio_path=split_path, serial_number=split_serial, event=self.event)

class Event:
    def __init__(self):
        self.data_objects = []

    def add_data_object(self, data_object):
        self.data_objects.append(data_object)

    def remove_data_object(self, data_object):
        self.data_objects.remove(data_object)

class AudioSplitter:
    def __init__(self, audio_data, split_duration_minutes):
        self.audio_data = audio_data
        self.split_duration_milliseconds = split_duration_minutes * 60 * 1000  # Convert to milliseconds

    def split_audio_data_object(self):
        # Set original audio serial number to X.0 format
        original_serial = f"{self.audio_data.serial_number}.0"
        self.audio_data.set_serial_number(original_serial)

        # Add original data object back to event with updated serial number
        self.audio_data.event.remove_data_object(self.audio_data)
        self.audio_data.event.add_data_object(self.audio_data)

        # Load the audio file
        audio = AudioSegment.from_file(self.audio_data.audio_path)
        total_duration = len(audio)  # Duration in milliseconds

        split_paths = []
        idx = 1
        for start_ms in range(0, total_duration, self.split_duration_milliseconds):
            end_ms = min(start_ms + self.split_duration_milliseconds, total_duration)
            split_audio = audio[start_ms:end_ms]
            split_path = f"{os.path.splitext(self.audio_data.audio_path)[0]}_{idx}.mp4a"
            split_audio.export(split_path, format="mp4a")
            split_paths.append(split_path)
            idx += 1

        # Create and add split data objects to event
        for idx, split_path in enumerate(split_paths, start=1):
            split_serial = f"{self.audio_data.serial_number}.{idx}"
            split_data_object = self.audio_data.create_split(split_path, split_serial)
            self.audio_data.event.add_data_object(split_data_object)

# Example usage:
event = Event()
audio_path = "C:\\Users\\LENOVO\\Downloads\\videoplayback (3).m4a"  # Update with audio path
original_audio = AudioData(audio_path=audio_path, serial_number="2", event=event)
event.add_data_object(original_audio)

audio_splitter = AudioSplitter(audio_data=original_audio, split_duration_minutes=5)
audio_splitter.split_audio_data_object()

# Print the new audio objects
for data_object in event.data_objects:
    print(data_object.serial_number, data_object.audio_path)

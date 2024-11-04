import contextlib
import os
import wave

from pydub import AudioSegment

from Engine.DataObjects.AudioDataObject import AudioData
from Engine.DataObjects.Event import EventData


class AudioPreprocessor:
    def __init__(self, audio_data: AudioData, event: EventData, split_duration_minutes: int):
        self.audio_data = audio_data
        self.split_duration_milliseconds = split_duration_minutes * 60 * 1000  # Convert to milliseconds
        self.event = event

    def check_integrity(self):
        """Check if the audio file is valid and not corrupted."""
        try:
            with contextlib.closing(wave.open(self.audio_data.audio_path, 'r')) as audio:
                frames = audio.getnframes()
                duration = frames / float(audio.getframerate())
                return duration > 0
        except Exception:
            return False

    def convert_to_mp3(self):
        """Convert audio file to MP3 format."""
        try:
            audio = AudioSegment.from_file(self.audio_data.audio_path)
            output_path = os.path.splitext(self.audio_data.audio_path)[0] + '.mp3'
            audio.export(output_path, format='mp3')
            return output_path
        except Exception as e:
            print(f"Error converting file: {e}")
            return None

    def split_audio_data(self):
        """Split the audio file into smaller segments."""
        if not self.audio_data.load_data():
            print("Failed to load audio data.")
            return

        # Set original audio serial number to X.0 format
        original_serial = f"{self.audio_data.get_serial_id()}.0"
        self.audio_data.set_serial_id(original_serial)

        # Create the splits
        audio = self.audio_data.get_audio()
        total_duration = len(audio)  # Duration in milliseconds
        idx = 1

        for start_ms in range(0, total_duration, self.split_duration_milliseconds):
            end_ms = min(start_ms + self.split_duration_milliseconds, total_duration)
            split_audio = audio[start_ms:end_ms]

            # Create the split file path
            split_path = f"{os.path.splitext(self.audio_data.get_path())[0]}_{idx}.mp3"  # Save as .mp3
            split_audio.export(split_path, format="mp3")  # Export format to mp3

            # Create a new AudioData object for the split audio
            split_serial = f"{original_serial}.{idx}"
            split_audio_data = AudioData(audio_path=split_path, event_id=self.audio_data.get_event_id())
            split_audio_data.set_serial_id(split_serial)

            # Add the new audio data object to the event
            self.event.add_data(split_audio_data)
            idx += 1

# # Example usage
# if __name__ == "__main__":
#     # Create an event data instance
#     monitor = Publisher()  # Assuming Publisher is already implemented
#     event_data = EventData(event_id="1", monitor=monitor)
#
#     # Load original audio data
#     audio_path = "C:\\Users\\LENOVO\\Downloads\\videoplayback (3).m4a"  # Update with the audio path
#     original_audio = AudioData(audio_path=audio_path, event_id=event_data.event_id)
#
#     # Create the audio preprocessor
#     audio_preprocessor = AudioPreprocessor(original_audio, event_data, split_duration_minutes=5)
#
#     # Part 1: Corruption Detection
#     if audio_preprocessor.check_integrity():
#         print("Audio file is valid.")
#     else:
#         print("Audio file is corrupted or invalid.")
#         exit()  # Stop execution if the file is invalid
#
#     # Part 2: Conversion to MP3
#     converted_path = audio_preprocessor.convert_to_mp3()
#     if converted_path:
#         print(f"Converted audio file saved at: {converted_path}")
#         original_audio.set_audio(converted_path)  # Update audio path to converted file
#
#     # Add original audio data to the event
#     event_data.add_data(original_audio)
#
#     # Part 3: Splitting the audio
#     audio_preprocessor.split_audio_data()
#
#     # Print the new audio objects
#     for data_object in event_data.get_all_data():
#         print(data_object.get_serial_id(), data_object.get_path())

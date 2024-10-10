from DataObjects.Base import BaseData
from pydub import AudioSegment


class AudioData(BaseData):
    def __init__(self, audio_path, event_id, serial_id):
        super().__init__(event_id, serial_id, "audio")
        self.audio_path = audio_path
        self.audio = None
        self.format = None
        self.duration = None

    def load_data(self):
        """Load the audio file when needed."""
        if self.audio is None:
            try:
                self.audio = AudioSegment.from_file(self.audio_path)
                self.format = self.audio.format
                self.duration = self.audio.duration_seconds
            except Exception as e:
                print(f"Error loading audio: {e}")
                return False
        return True

    def get_context(self):
        return super().context

    def get_audio(self):
        if self._load_audio():
            return self.audio
        return None

    def get_format(self):
        if self._load_audio():
            return self.format
        return None

    def get_duration(self):
        if self._load_audio():
            return self.duration
        return None

    def set_context(self, text):
        try:
            super().context = text
            return True
        except Exception as e:
            print(f"Error setting context: {e}")
            return False

    def set_audio(self, audio_path):
        self.audio_path = audio_path
        self.audio = None
        self.format = None
        self.duration = None
        return True

    def set_corrupted(self):
        self.corrupted = True

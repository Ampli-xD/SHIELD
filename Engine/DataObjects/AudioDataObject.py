from pydub import AudioSegment

from Engine.DataObjects.Base import BaseData


class AudioData(BaseData):
    def __init__(self, audio_path, event_id):
        super().__init__(event_id, "audio")
        self.audio_path = audio_path
        self.audio = None
        self.format = None
        self.duration = None

    def load_data(self):
        """Load the audio file when needed."""
        if self.audio is None:
            try:
                print(self.audio_path)
                self.audio = AudioSegment.from_file(self.audio_path)
                self.format = self.audio.format
                self.duration = self.audio.duration_seconds
            except Exception as e:
                print(f"Error loading audio: {e}")
                return False
        return True

    def get_context(self):
        return self.context

    def get_audio(self):
        if self.load_data():
            return self.audio
        return None

    def get_format(self):
        if self.load_data():
            return self.format
        return None

    def get_duration(self):
        if self.load_data():
            return self.duration
        return None

    def set_context(self, text):
        try:
            self.context = text
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

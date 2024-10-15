import wave
import os
import contextlib
from pydub import AudioSegment

class AudioCorruptionDetector:
    def __init__(self):
        pass

class AudioCorruptionDetector:
    def check_integrity(self, audio_data):
        try:
            with contextlib.closing(wave.open(audio_data.file_path, 'r')) as audio:
                frames = audio.getnframes()
                duration = frames / float(audio.getframerate())
                return duration > 0
        except Exception:
            return False

    def convert_format(self, audio_data, output_format='mp3'):
        try:
            audio = AudioSegment.from_file(audio_data.file_path)
            output_path = os.path.splitext(audio_data.file_path)[0] + f'.{output_format}'
            audio.export(output_path, format=output_format)
            return output_path
        except Exception:
            return None


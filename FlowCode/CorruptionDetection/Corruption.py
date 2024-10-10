import os
from PIL import Image
import cv2
import wave
import contextlib

class CorruptionDetector:
    def __init__(self, event_data):
        self.event_data = event_data
        self.corrupted_items = [] 
         

    def check_text_integrity(self, text_data):
  
        if os.path.exists(text_data.text_content):
            with open(text_data.text_content, 'r', encoding='utf-8') as file:
                content = file.read().strip()
            return bool(content)  
        return False  

    def check_image_integrity(self, image_data):
        try:
            with Image.open(image_data.image_path) as img:
                img.verify()
            return True
        except Exception:
            return False

    def check_audio_integrity(self, audio_data):
        try:
            with contextlib.closing(wave.open(audio_data.audio_path, 'r')) as audio:
                frames = audio.getnframes()
                duration = frames / float(audio.getframerate())
                return duration > 0
        except Exception:
            return False

    def check_video_integrity(self, video_data):
        try:
            cap = cv2.VideoCapture(video_data.video_path)
            if not cap.isOpened():
                return False
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            cap.release()
            return frame_count > 0
        except Exception:
            return False

    def is_corrupted(self, data_object):
        # Determine the type and apply the appropriate check
        if isinstance(data_object, TextData):
            if not self.check_text_integrity(data_object):
                self.mark_corrupted(data_object)
        elif isinstance(data_object, ImageData):
            if not self.check_image_integrity(data_object):
                self.mark_corrupted(data_object)
        elif isinstance(data_object, AudioData):
            if not self.check_audio_integrity(data_object):
                self.mark_corrupted(data_object)
        elif isinstance(data_object, VideoData):
            if not self.check_video_integrity(data_object):
                self.mark_corrupted(data_object)

    def mark_corrupted(self, data_object):
        data_object.set_corrupted()
        self.corrupted_items.append(data_object)

    def process_all(self):
        for data_object in self.event_data.data_objects:
            data_object.load_data()
            self.is_corrupted(data_object)

        return self.corrupted_items  
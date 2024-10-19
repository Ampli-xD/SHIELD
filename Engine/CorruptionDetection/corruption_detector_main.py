from audio_corruption_detector import AudioCorruptionDetector
from image_corruption_detector import ImageCorruptionDetector
from text_corruption_detector import TextCorruptionDetector
from video_corruption_detector import VideoCorruptionDetector


class CorruptionDetector:
    def __init__(self, event_data):
        self.event_data = event_data
        self.corrupted_items = []
        
        self.text_detector = TextCorruptionDetector()
        self.image_detector = ImageCorruptionDetector()
        self.audio_detector = AudioCorruptionDetector()
        self.video_detector = VideoCorruptionDetector()

    def is_corrupted(self, data_object):
        data_type = data_object.data_type
        if data_type == "text":
            if not self.text_detector.check_integrity(data_object):
                self.mark_corrupted(data_object)
        elif data_type == "image":
            if not self.image_detector.check_integrity(data_object):
                self.mark_corrupted(data_object)
        elif data_type == "audio":
            if not self.audio_detector.check_integrity(data_object):
                self.mark_corrupted(data_object)
        elif data_type == "video":
            if not self.video_detector.check_integrity(data_object):
                self.mark_corrupted(data_object)

    def mark_corrupted(self, data_object):
        data_object.corrupted = True
        self.corrupted_items.append(data_object)

    def process_all(self):
        for data_object in self.event_data.data_objects:
            data_object.load_data()
            self.is_corrupted(data_object)
        return self.corrupted_items

    def convert_text(self, text_data):
        return self.text_detector.convert_text_to_upper(text_data)

    def convert_image(self, image_data, output_format='PNG'):
        return self.image_detector.convert_format(image_data, output_format)

    def convert_audio(self, audio_data, output_format='mp3'):
        return self.audio_detector.convert_format(audio_data, output_format)

    def convert_video(self, video_data, output_format='avi'):
        return self.video_detector.convert_format(video_data, output_format)

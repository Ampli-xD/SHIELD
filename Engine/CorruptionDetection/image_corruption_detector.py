from PIL import Image
import os

class ImageCorruptionDetector:
    def __init__(self):
        pass

class ImageCorruptionDetector:
    def check_integrity(self, image_data):
        try:
            with Image.open(image_data.file_path) as img:
                img.verify()
            return True
        except Exception:
            return False

    def convert_format(self, image_data, output_format='PNG'):
        try:
            with Image.open(image_data.file_path) as img:
                output_path = os.path.splitext(image_data.file_path)[0] + f'.{output_format.lower()}'
                img.save(output_path, format=output_format)
            return output_path
        except Exception:
            return None

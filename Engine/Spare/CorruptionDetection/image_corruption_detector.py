import os

from PIL import Image


class ImageCorruptionDetector:
    def __init__(self):
        pass

    @staticmethod
    def check_integrity(image_data):
        try:
            with Image.open(image_data.file_path) as img:
                img.verify()
            return True
        except Exception:
            return False

    @staticmethod
    def convert_format(image_data, output_format='PNG'):
        try:
            with Image.open(image_data.file_path) as img:
                output_path = os.path.splitext(image_data.file_path)[0] + f'.{output_format.lower()}'
                img.save(output_path, format=output_format)
            return output_path
        except Exception:
            return None

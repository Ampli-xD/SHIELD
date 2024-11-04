import os


class TextCorruptionDetector:
    def __init__(self):
        pass

    @staticmethod
    def check_integrity(text_data):
        if os.path.exists(text_data.file_path):
            with open(text_data.file_path, 'r', encoding='utf-8') as file:
                content = file.read().strip()
            return bool(content)
        return False

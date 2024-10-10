from DataObjects.Base import BaseData
from PIL import Image


class ImageData(BaseData):
    def __init__(self, image_path, event_id, serial_id):
        super().__init__(event_id, serial_id, "image")
        self.image_path = image_path
        self.image = None
        self.format = None
        self.size = None

    def load_data(self):
        if self.image is None:
            try:
                self.image = Image.open(self.image_path)
                self.format = self.image.format
                self.size = self.image.size
            except Exception as e:
                print(f"Error loading image: {e}")
                return False
        return True

    def get_context(self):
        return super().context

    def get_image(self):
        if self._load_image():
            return self.image
        return None

    def get_format(self):
        if self._load_image():
            return self.format
        return None

    def get_size(self):
        if self._load_image():
            return self.size
        return None

    def set_context(self, text):
        try:
            super().context = text
            return True
        except Exception as e:
            print(f"Error setting context: {e}")
            return False

    def set_image(self, image_path):
        self.image_path = image_path
        self.image = None
        self.format = None
        self.size = None
        return True

    def set_corrupted(self):
        self.corrupted = True

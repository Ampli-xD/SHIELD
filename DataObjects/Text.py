from DataObjects.Base import BaseData


class TextData(BaseData):
    def __init__(self, text_content, event_id, serial_id):
        super().__init__(event_id, serial_id, "text")
        self.text_content = text_content

    def get_context(self):
        return super().context

    def get_text(self):
        return self.text_content

    def set_context(self, text):
        try:
            super().context = text
            return True
        except Exception as e:
            print(f"Error setting context: {e}")
            return False

    def set_text(self, text_content):
        self.text_content = text_content

    def set_corrupted(self):
        self.corrupted = True

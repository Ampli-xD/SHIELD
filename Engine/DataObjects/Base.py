class BaseData:
    def __init__(self, event_id, data_type):
        self.event_id = event_id
        self.data_type = data_type
        self.serial_id = None
        self.parent_prompt = None
        self.context = None
        self.corrupted = False

    def get_event_id(self):
        return self.event_id

    def get_serial_id(self):
        return self.serial_id

    def get_data_type(self):
        return self.data_type

    def get_context(self):
        return self.context

    def set_event_id(self, event_id):
        self.event_id = event_id
        return True

    def set_serial_id(self, serial_id):
        self.serial_id = serial_id
        return True

    def set_data_type(self, data_type):
        self.data_type = data_type
        return True

    def set_corrupted(self):
        self.corrupted = True





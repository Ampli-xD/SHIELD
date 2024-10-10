class EventData:
    def __init__(self, event_id):
        self.event_id = event_id
        self.data_items = []
        self.serial_counter = 0

    def add_data(self, data_object):
        """Adds a new data object to the event, assigning a serial ID."""
        self.serial_counter += 1
        data_object.serial_id = self.serial_counter
        self.data_items.append(data_object)

    def get_data_by_serial(self, serial_id):
        """Fetches data object by its serial ID."""
        for item in self.data_items:
            if item.serial_id == serial_id:
                return item
        return None

    def get_data_by_type(self, data_type):
        """Fetches all data objects of a specific type."""
        return [item for item in self.data_items if item.data_type == data_type]

    def get_all_data(self):
        """Returns all data objects in the event."""
        return self.data_items

    def clear_data(self):
        try:
            self.data_items = []
            return True
        except:
            return False

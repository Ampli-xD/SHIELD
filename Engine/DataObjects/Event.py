from Engine.DataObjects.Base import BaseData
from Runner.Monitor.PubSub import Publisher


class EventData:
    def __init__(self, event_id, monitor: Publisher):
        self.event_id = event_id
        self.data_items = []
        self.serial_counter = 0
        self.combined_text = None
        self.module = "EventData Module"
        self.monitor = monitor

    def add_data(self, data_object: BaseData):
        """Adds a new data object to the event, assigning a serial ID."""
        self.serial_counter += 1
        data_object.serial_id = self.serial_counter
        self.data_items.append(data_object)
        formatted_objective = f"Data object added ({data_object.get_data_type()} with serial id {self.event_id}.{data_object.get_serial_id()})"
        try:
            self.monitor.publish(objective=formatted_objective, module=self.module)
        except Exception as e:
            print(e)

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

    def get_number_of_data_objects(self):
        return self.serial_counter

    def set_combined_text(self, text):
        self.combined_text = text

    def get_combined_text(self):
        return self.combined_text

    def clear_data(self):
        try:
            self.data_items = []
            return True
        except:
            return False

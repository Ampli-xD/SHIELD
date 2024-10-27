from Engine.DataObjects.Event import EventData


class ContextCombiner:
    def __init__(self):
        self.length = None
        self.final_context = ""

    def combine_contexts(self, event: EventData):
        self.length = event.serial_counter
        data_in_event = event.get_all_data()
        for i in range(0, self.length):
            details_update = self.details_adder(data_in_event[i])
            self.final_context += details_update
        event.set_combined_text(self.final_context)

    @staticmethod
    def details_adder(data_object):
        return f"""
serial_id: {data_object.event_id}.{data_object.serial_id} {data_object.data_type}

{str(data_object.get_context())}


"""

    def get_final_context(self):
        return self.final_context

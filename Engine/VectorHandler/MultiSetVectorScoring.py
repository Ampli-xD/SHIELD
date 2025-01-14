from Engine.DataObjects.Event import EventData
from Engine.VectorHandler.VectorScoring import VectorBasedScoringSystem
from Runner.Monitor.PubSub import Publisher


class VectorScoring:
    def __init__(self, path, monitor: Publisher):
        self.monitor = monitor
        self.vec_score_sys = VectorBasedScoringSystem(monitor, path=path)
        self.final_json = []

    def get_vector_scores(self, event: EventData):
        self.final_json = []

        overall = event.get_combined_text()
        data_objects = event.get_all_data()

        for i in data_objects:
            data_serial_id = f"{i.event_id}.{i.serial_id}"
            data_object_score = self.vec_score_sys.score_text_by_vectors(i.get_context())
            data_set = {
                "serial_id": data_serial_id,
                "score": data_object_score
            }
            data_set1 = {
                "serial_id": data_serial_id,
                "filename": i.get_filename(),
                "score": data_object_score
            }
            self.monitor.publish(objective=f"Scored, ID {data_serial_id}", module="Vector Scoring", data=data_set1)
            self.final_json.append(data_set)

        combine_text_results = self.vec_score_sys.score_text_by_vectors(overall)
        self.final_json.append({
            "serial_id": "OVERALL",
            "score": combine_text_results
        })

        return self.final_json

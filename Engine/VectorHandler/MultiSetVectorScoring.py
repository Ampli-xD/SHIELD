from Engine.DataObjects.Event import EventData
from Engine.VectorHandler.VectorScoring import VectorBasedScoringSystem


class VectorScoring:
    def __init__(self, path):
        self.vec_score_sys = VectorBasedScoringSystem(path=path)
        self.final_json = []

    def get_vector_scores(self, event: EventData):
        self.final_json = []

        overall = event.get_combined_text()
        data_objects = event.get_all_data()

        for i in data_objects:
            data_serial_id = f"{i.event_id}.{i.serial_id}"
            data_object_score = self.vec_score_sys.score_vectors(i.get_context())
            self.final_json.append({
                "serial_id": data_serial_id,
                "score": data_object_score
            })

        combine_text_results = self.vec_score_sys.score_vectors(overall)
        self.final_json.append({
            "serial_id": "OVERALL",
            "score": combine_text_results
        })

        return self.final_json

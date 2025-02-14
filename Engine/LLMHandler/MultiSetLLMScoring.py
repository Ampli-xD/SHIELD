import time

from Engine.DataObjects.Event import EventData
from Engine.LLMHandler.LLMCaller import LLMGenerator
from Engine.LLMHandler.LLMPrompts import SingleAnalysisPrompt
from Runner.Monitor.PubSub import Publisher


class LLMScoring:
    def __init__(self, api_key, monitor: Publisher):
        self.llm_generator = LLMGenerator(api_key)
        self.final_json = []
        self.monitor = monitor

    def get_llm_scores(self, event: EventData):
        self.final_json = []

        overall = event.get_combined_text()
        data_objects = event.get_all_data()

        for i in data_objects:
            start_time = time.time()
            data_serial_id = f"{i.event_id}.{i.serial_id}"
            data_object_score = self.llm_generator.score_text_by_llm(i.get_context(),
                                                                     system_prompt=SingleAnalysisPrompt)
            end_time = time.time()

            data_set = {
                "serial_id": data_serial_id,
                "score": data_object_score
            }
            data_set1 = {
                "serial_id": data_serial_id,
                "filename": i.get_filename(),
                "score": data_object_score,
                "type": "LLMScoring",
                "time": f"{end_time - start_time: .6f}"
            }
            self.monitor.publish(objective=f"Scored, ID {data_serial_id}", module="LLM Scoring", data=data_set1)
            self.final_json.append(data_set)

        combine_text_results = self.llm_generator.score_text_by_llm(overall, system_prompt=SingleAnalysisPrompt)
        self.final_json.append({
            "serial_id": "OVERALL",
            "score": combine_text_results
        })

        return self.final_json

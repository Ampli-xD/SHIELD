import os

from Engine.LLMHandler.MultiSetLLMScoring import LLMScoring
from Engine.Processors import AudioProcessing, ImageProcessing, VideoProcessing
from Engine.Processors.TextProcessing import ContextCombiner
from Engine.VectorHandler.MultiSetVectorScoring import VectorScoring


class TaskPerformer:
    def __init__(self, event, monitor):
        self.event = event
        self.monitor = monitor

    def perform_tasks(self):
        self._process_data()
        self._combine_contexts()
        json_vector_response, json_llm_response = self._get_scores()
        return json_vector_response, json_llm_response

    def _process_data(self):
        api_key = "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"
        api_key = "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"
        audio_processor = AudioProcessing.AudioProcessor(api_key, self.monitor)
        image_processor = ImageProcessing.ImageProcessor(api_key, self.monitor)
        video_processor = VideoProcessing.VideoProcessor("AIzaSyD9ygld0-1qZsYekMoOrZYFGDPuEfDD7xA", self.monitor)

        for data_object in self.event.get_all_data():
            if data_object.get_data_type() == 'video':
                video_processor.fetch_video_analysis(data_object)
            elif data_object.get_data_type() == 'audio':
                audio_processor.fetch_audio_transcription(data_object)
            elif data_object.get_data_type() == 'image':
                image_processor.fetch_image_analysis(data_object)

    def _combine_contexts(self):
        combiner = ContextCombiner()
        combiner.combine_contexts(self.event)

    def _get_scores(self):
        api_key = "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"
        api_key = "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"
        llm_scorer = LLMScoring(api_key, self.monitor)
        ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        vector_scorer = VectorScoring(
            path=os.path.join(ROOT_DIR, "Engine", "VectorHandler", "persistent_chroma_db"),
            monitor=self.monitor
        )
        # vector_scorer = VectorScoring(path="../../Engine/VectorHandler/persistent_chroma_db", monitor=self.monitor)

        json_vector_response = vector_scorer.get_vector_scores(self.event)
        json_llm_response = llm_scorer.get_llm_scores(self.event)

        return json_vector_response, json_llm_response
        # Process or print the responses as needed

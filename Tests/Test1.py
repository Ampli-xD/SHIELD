import os.path
from pathlib import Path

from Engine.DataObjects import ImageDataObject, VideoDataObject, Event, TextDataObject, AudioDataObject
from Engine.LLMHandler.LLMCaller import LLMGenerator
from Engine.Processors import AudioProcessing, ImageProcessing, VideoProcessing
from Engine.Processors.TextProcessing import ContextCombiner

AUDIO_EXTENSIONS = {'.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.wav', '.webm'}
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif'}
TEXT_EXTENSIONS = {'.txt'}
VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv', '.flv'}


def segregate_files(folder_path, event_object):
    for file in Path(folder_path).iterdir():
        if file.is_file():
            ext = file.suffix.lower()
            if ext in AUDIO_EXTENSIONS:
                audio_object = AudioDataObject.AudioData(file, event_object.event_id)
                event_object.add_data(audio_object)
            elif ext in IMAGE_EXTENSIONS:
                image_object = ImageDataObject.ImageData(file, event_object.event_id)
                event_object.add_data(image_object)
            elif ext in TEXT_EXTENSIONS:
                text_object = TextDataObject.TextData(file, event_object.event_id)
                event_object.add_data(text_object)
            elif ext in VIDEO_EXTENSIONS:
                video_object = VideoDataObject.VideoData(file, event_object.event_id)
                event_object.add_data(video_object)


def perform_tasks(folder_path):
    event = Event.EventData(event_id=1234)
    segregate_files(folder_path, event)
    api_key = "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"
    audio_processor = AudioProcessing.AudioProcessor(api_key)
    image_processor = ImageProcessing.ImageProcessor(api_key)
    video_processor = VideoProcessing.VideoProcessor("AIzaSyD9ygld0-1qZsYekMoOrZYFGDPuEfDD7xA")
    llm_generator = LLMGenerator(api_key)

    for i in event.get_all_data():
        if i.get_data_type() == 'video':
            video_processor.fetch_video_analysis(i)
        elif i.get_data_type() == 'audio':
            audio_processor.fetch_audio_transcription(i)
        elif i.get_data_type() == 'image':
            image_processor.fetch_image_analysis(i)

    # for i in event.get_data_by_type('video'):
    #     video_processor.fetch_video_analysis(i)
    #     # print(i.get_path())
    #     # print(i.context)
    #
    # for i in event.get_data_by_type('audio'):
    #     # print(i.audio_path)
    #     audio_processor.fetch_audio_transcription(i)
    #     # print(i.context)
    #
    # for i in event.get_data_by_type('image'):
    #     image_processor.fetch_image_analysis(i)
    #     # print(i.image_path)
    #     # print(i.context)

    combiner = ContextCombiner()
    combiner.combine_contexts(event)
    print(combiner.get_final_context())
    response = llm_generator.generate_text(combiner.get_final_context())
    print(response)


if __name__ == "__main__":
    folder_path = os.path.dirname(__file__) + '/DO_NOT_OPEN/'
    perform_tasks(folder_path)

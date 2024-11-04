from pathlib import Path

from Engine.DataObjects import AudioDataObject, ImageDataObject, TextDataObject, VideoDataObject


class FileSegregator:
    AUDIO_EXTENSIONS = {'.mp3', '.mpeg', '.mpga', '.m4a', '.wav', '.webm'}
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif'}
    TEXT_EXTENSIONS = {'.txt'}
    VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv', '.flv'}

    def __init__(self, folder_path, event_object, monitor):
        self.monitor = monitor
        self.folder_path = folder_path
        self.event_object = event_object

    def segregate_files(self):
        try:
            # Create a Path object with the absolute folder path
            self.monitor.publish(objective="Segregating Files...", module="LOG (FileSegregator)")
            folder_path = Path(self.folder_path).resolve()

            # Check if the path exists and is a directory
            if not folder_path.is_dir():
                self.monitor.publish(
                    objective=f"Error: The folder path '{folder_path}' does not exist or is not a directory.",
                    module="LOG (FileSegregator)")
                print(f"Error: The folder path '{folder_path}' does not exist or is not a directory.")
                return False

            # Iterate through files in the specified folder
            for file in folder_path.iterdir():
                if file.is_file():
                    ext = file.suffix.lower()
                    self._add_file_to_event(file, ext)

            return True  # Return True if files are processed
        except Exception as e:
            print(f"Error during file segregation: {str(e)}")
            return False

    def _add_file_to_event(self, file, ext):
        if ext in self.AUDIO_EXTENSIONS:
            audio_object = AudioDataObject.AudioData(file, self.event_object.event_id)
            self.event_object.add_data(audio_object)
        elif ext in self.IMAGE_EXTENSIONS:
            image_object = ImageDataObject.ImageData(file, self.event_object.event_id)
            self.event_object.add_data(image_object)
        elif ext in self.TEXT_EXTENSIONS:
            text_object = TextDataObject.TextData(file, self.event_object.event_id)
            self.event_object.add_data(text_object)
        elif ext in self.VIDEO_EXTENSIONS:
            video_object = VideoDataObject.VideoData(file, self.event_object.event_id)
            self.event_object.add_data(video_object)

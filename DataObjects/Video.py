from DataObjects.Base import BaseData
import cv2


class VideoData(BaseData):
    def __init__(self, video_path, event_id, serial_id):
        super().__init__(event_id, serial_id, "video")
        self.video_path = video_path
        self.video = None
        self.format = None
        self.frame_count = None
        self.fps = None

    def load_data(self):
        if self.video is None:
            try:
                self.video = cv2.VideoCapture(self.video_path)
                if self.video.isOpened():
                    self.format = self.video.get(cv2.CAP_PROP_FOURCC)
                    self.frame_count = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
                    self.fps = self.video.get(cv2.CAP_PROP_FPS)
                else:
                    print("Error: Cannot open video file.")
                    self.video = None
            except Exception as e:
                print(f"Error loading video: {e}")
                return False
        return True

    def get_context(self):
        return super().context

    def get_video(self):
        if self._load_video():
            return self.video
        return None

    def get_format(self):
        if self._load_video():
            return self.format
        return None

    def get_frame_count(self):
        if self._load_video():
            return self.frame_count
        return None

    def get_fps(self):
        if self._load_video():
            return self.fps
        return None

    def set_context(self, text):
        try:
            super().context = text
            return True
        except Exception as e:
            print(f"Error setting context: {e}")
            return False

    def set_video(self, video_path):
        if self.video:
            self.video.release()
        self.video_path = video_path
        self.video = None
        self.format = None
        self.frame_count = None
        self.fps = None
        return True

    def set_corrupted(self):
        self.corrupted = True

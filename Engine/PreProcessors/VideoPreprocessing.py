import os

import cv2

from Engine.DataObjects.Event import EventData
from Engine.DataObjects.VideoDataObject import VideoData  # Assuming this exists


class VideoPreprocessor:
    def __init__(self, video_data: VideoData, event: EventData, split_duration_minutes: int):
        self.video_data = video_data
        self.split_duration_seconds = split_duration_minutes * 60  # Convert to seconds
        self.event = event

    def check_integrity(self):
        """Check if the video file is valid and not corrupted."""
        try:
            cap = cv2.VideoCapture(self.video_data.video_path)
            return cap.isOpened() and int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) > 0
        except Exception:
            return False

    def convert_to_mp4(self):
        """Convert video file to MP4 format."""
        try:
            cap = cv2.VideoCapture(self.video_data.video_path)
            output_path = os.path.splitext(self.video_data.video_path)[0] + '.mp4'
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, cap.get(cv2.CAP_PROP_FPS),
                                  (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                                   int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                out.write(frame)
            cap.release()
            out.release()
            return output_path
        except Exception as e:
            print(f"Error converting video file: {e}")
            return None

    def split_video_data(self):
        """Split the video file into smaller segments."""
        if not self.video_data.load_data():
            print("Failed to load video data.")
            return

        original_serial = f"{self.video_data.get_serial_id()}.0"
        self.video_data.set_serial_id(original_serial)

        with cv2.VideoCapture(self.video_data.video_path) as cap:
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            split_frames = int(fps * self.split_duration_seconds)

            idx = 1
            for start_frame in range(0, total_frames, split_frames):
                cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
                split_path = f"{os.path.splitext(self.video_data.video_path)[0]}_{idx}.mp4"
                fourcc = cv2.VideoWriter_fourcc(*"mp4v")

                with cv2.VideoWriter(split_path, fourcc, fps, (width, height)) as out:
                    frames_written = 0

                    while frames_written < split_frames:
                        ret, frame = cap.read()
                        if not ret:
                            break
                        out.write(frame)
                        frames_written += 1

                idx += 1

        # Create and add split data objects to event
        for i in range(1, idx):
            split_serial = f"{original_serial}.{i}"
            split_video_data = VideoData(video_path=f"{os.path.splitext(self.video_data.video_path)[0]}_{i}.mp4",
                                         event_id=self.video_data.get_event_id())
            split_video_data.set_serial_id(split_serial)
            self.event.add_data(split_video_data)

# # Example usage
# if __name__ == "__main__":
#     # Create an event data instance
#     monitor = Publisher()  # Assuming Publisher is already implemented
#     event_data = EventData(event_id="1", monitor=monitor)
#
#     # Load original video data
#     video_path = "C:\\Users\\LENOVO\\Downloads\\video.mp4"  # Update with video path
#     original_video = VideoData(video_path=video_path, event_id=event_data.event_id)
#
#     # Create the video preprocessor
#     video_preprocessor = VideoPreprocessor(original_video, event_data, split_duration_minutes=5)
#
#     # Part 1: Corruption Detection for Video
#     if video_preprocessor.check_integrity():
#         print("Video file is valid.")
#     else:
#         print("Video file is corrupted or invalid.")
#         exit()
#
#     # Part 2: Conversion to MP4
#     converted_video_path = video_preprocessor.convert_to_mp4()
#     if converted_video_path:
#         print(f"Converted video file saved at: {converted_video_path}")
#         original_video.set_video(converted_video_path)
#
#     # Add original video data to the event
#     event_data.add_data(original_video)
#
#     # Part 3: Splitting the video
#     video_preprocessor.split_video_data()
#
#     # Print the new video objects
#     print("Video Data Objects:")
#     for data_object in event_data.get_all_data():
#         print(data_object.get_serial_id(), data_object.get_path())

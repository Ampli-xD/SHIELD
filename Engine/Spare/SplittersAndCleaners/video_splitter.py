import os

import cv2


# Define the VideoData class
class VideoData:
    def __init__(self, video_path, serial_number, event):
        self.video_path = video_path
        self.serial_number = serial_number
        self.event = event

    def load_data(self):
        pass  # Placeholder for future processing if needed

    def set_serial_number(self, new_serial):
        self.serial_number = new_serial

    def create_split(self, split_path, split_serial):
        return VideoData(video_path=split_path, serial_number=split_serial, event=self.event)

# Define the Event class to manage data objects
class Event:
    def __init__(self):
        self.data_objects = []

    def add_data_object(self, data_object):
        self.data_objects.append(data_object)

    def remove_data_object(self, data_object):
        self.data_objects.remove(data_object)

# Define the VideoSplitter class to handle splitting
class VideoSplitter:
    def __init__(self, video_data, split_duration_minutes):
        self.video_data = video_data
        self.split_duration_minutes = split_duration_minutes * 60  # Convert minutes to seconds

    def split_video_data_object(self):
        # Set original video serial number to X.0 format
        original_serial = f"{self.video_data.serial_number}.0"
        self.video_data.set_serial_number(original_serial)

        # Add original data object back to event with updated serial number
        self.video_data.event.remove_data_object(self.video_data)
        self.video_data.event.add_data_object(self.video_data)

        cap = cv2.VideoCapture(self.video_data.video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        split_frames = int(fps * self.split_duration_minutes)

        split_paths = []
        idx = 1
        for start_frame in range(0, total_frames, split_frames):
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
            split_path = f"{os.path.splitext(self.video_data.video_path)[0]}_{idx}.mp4"
            split_paths.append(split_path)

            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            out = cv2.VideoWriter(split_path, fourcc, fps, (int(cap.get(3)), int(cap.get(4))))
            frames_written = 0

            while frames_written < split_frames and cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                out.write(frame)
                frames_written += 1

            out.release()
            idx += 1

        cap.release()

        # Create and add split data objects to event
        for idx, split_path in enumerate(split_paths, start=1):
            split_serial = f"{self.video_data.serial_number}.{idx}"
            split_data_object = self.video_data.create_split(split_path, split_serial)
            self.video_data.event.add_data_object(split_data_object)
            
video_path = "path"  # Update this line with video's path
event = Event()
original_video = VideoData(video_path=video_path, serial_number="2", event=event)
event.add_data_object(original_video)

video_splitter = VideoSplitter(video_data=original_video, split_duration_minutes=5)
video_splitter.split_video_data_object()

for data_object in event.data_objects:
    print(data_object.serial_number, data_object.video_path)
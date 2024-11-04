import os

import cv2


class VideoCorruptionDetector:
    def __init__(self):
        pass

    @staticmethod
    def check_integrity(video_data):
        try:
            cap = cv2.VideoCapture(video_data.file_path)
            if not cap.isOpened():
                return False
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            cap.release()
            return frame_count > 0
        except Exception:
            return False

    @staticmethod
    def convert_format(video_data, output_format='avi'):
        try:
            cap = cv2.VideoCapture(video_data.file_path)
            output_path = os.path.splitext(video_data.file_path)[0] + f'.{output_format}'
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
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
        except Exception:
            return None

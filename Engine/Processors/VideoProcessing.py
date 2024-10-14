import time

import google.generativeai as genai


class VideoProcessor:
    def __init__(self, api_key):
        self.video_data = None
        genai.configure(api_key=api_key)

    def upload_video(self):
        genai.upload_file(self.video_data.get_path())
        return True

    def fetch_video_analysis(self, video_data_object):
        self.video_data = video_data_object
        try:
            uploaded_video = self.upload_video()

            while uploaded_video.state == "PROCESSING":
                print("Processing video...")
                time.sleep(5)

                uploaded_video = genai.get_file(uploaded_video.name)

            model = genai.GenerativeModel(model_name="gemini-1.5-pro-002")
            print("Making LLM inference request...")
            prompt = "Elaborate this in depth without missing any details in your response."
            response = model.generate_content([prompt, uploaded_video], request_options={"timeout": 600})

            self.update_context(response.text)

        except Exception as e:
            print(f"Error during video analysis: {e}")

    def update_context(self, text):
        if not self.video_data.set_context(text):
            raise Exception("Failed to update the context.")

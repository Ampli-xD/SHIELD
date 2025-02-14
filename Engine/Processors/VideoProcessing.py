import time

import google.generativeai as genai


class VideoProcessor:
    def __init__(self, api_key, monitor):
        self.monitor = monitor
        self.video_data = None
        genai.configure(api_key=api_key)

    def upload_video(self):
        # Upload the file and return the file object directly
        uploaded_file = genai.upload_file(self.video_data.get_path())
        time.sleep(5)
        # print(f"Debug: Uploaded video name is '{uploaded_file.name}'")
        return uploaded_file

    def fetch_video_analysis(self, video_data_object):
        self.monitor.publish(objective="Fetching Video Analysis...", module="LOG (VideoProcessor)")
        self.video_data = video_data_object
        try:
            uploaded_video = self.upload_video()
            # processing_complete = False

            # Polling with a manual "processing" check
            while True:
                try:
                    uploaded_video = genai.get_file(uploaded_video.name)
                    self.monitor.publish(objective="Fetched Video Analysis...", module="LOG (VideoProcessor)")
                    break
                except:
                    pass
                    # try:
                    #     uploaded_video = genai.get_file(uploaded_video.name)
                    #     self.monitor.publish(objective="Fetched Video Analysis...", module="LOG (VideoProcessor)")
                    # except:
                    #     uploaded_video = self.upload_video()
                    #     uploaded_video = genai.get_file(uploaded_video.name)
                    #     self.monitor.publish(objective="Fetched Video Analysis...", module="LOG (VideoProcessor)")

                # Check if processing is complete (adjust based on API response)
                # if self.is_processing_complete(uploaded_video):
                #     processing_complete = True

            model = genai.GenerativeModel(model_name="gemini-1.5-pro-002")
            prompt = f"Analyze the video named '{uploaded_video.name}' in depth without missing any details."
            # print(f"Debug: Prompt for LLM: {prompt}")

            # Generate content with only the prompt text
            response = model.generate_content([uploaded_video, prompt], request_options={"timeout": 600})
            # print(f"Response is {response.text}")
            self.update_context(response.text)

        except Exception as e:
            print(f"Error during video analysis: {e}")

    # def is_processing_complete(self, file_obj):
    #     # Placeholder for actual processing completion check.
    #     # Replace this with the real condition based on file_obj's attributes.
    #     # print("Debug: Checking if processing is complete...")
    #     # For demonstration purposes, we assume it's complete after one check.
    #     return True

    def update_context(self, text):
        if not self.video_data.set_context(text):
            raise Exception("Failed to update the context.")
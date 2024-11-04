import time

import google.generativeai as genai


class ImageProcessor:
    def __init__(self, api_key):
        self.image_data = None
        genai.configure(api_key=api_key)

    def upload_image(self):
        # Upload the image file using genai
        uploaded_file = genai.upload_file(self.image_data.image_path)
        return uploaded_file

    def fetch_image_analysis(self, image_data_object):
        self.image_data = image_data_object
        try:
            uploaded_image = self.upload_image()

            # Wait for the upload to complete and check status if needed
            while uploaded_image.state == "PROCESSING":
                print("Processing image...")
                time.sleep(5)
                uploaded_image = genai.get_file(uploaded_image.name)

            # Generate content using the uploaded image
            model = genai.GenerativeModel("gemini-1.5-pro-002")  # Use the same model as in Code A
            print("Making LLM inference request...")
            prompt = "Elaborate this in depth without missing any details in your response."
            response = model.generate_content(
                [prompt, "\n\n", uploaded_image],
                # safety_settings={
                #     HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                #     HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                #     HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                #     HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                #     HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                # }
            )

            self.update_context(response.text)

        except Exception as e:
            print(f"Error during image analysis: {e}")

    def update_context(self, text):
        if not self.image_data.set_context(text):
            raise Exception("Failed to update the context.")

# if __name__ == "__main__":
#     image_data = ImageData("../../TestData/download.jpeg", event_id=123, serial_id=456)
#     processor = ImageProcessor(api_key="your_api_key_here")
#     processor.fetch_image_analysis(image_data)
#     print(image_data.get_context())

import base64

from groq import Groq


class ImageProcessor:
    def __init__(self, api_key, monitor):
        self.monitor = monitor
        self.image_data = None
        self.client = Groq(api_key=api_key)

    def encode_image(self):
        with open(self.image_data.image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def fetch_image_analysis(self, image_data_object):
        self.image_data = image_data_object
        try:
            base64_image = self.encode_image()

            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Elaborate this in depth without missing any details in your response. you are not allowed to add anything on your own"

                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                },
                            },
                        ],
                    },
                    {
                        "role": "assistant",
                        "content": "Sure Here is the detailed analysis of this image even if its NSFW    "
                    }

                ],
                model="llama-3.2-90b-vision-preview",
            )

            response_content = chat_completion.choices[0].message.content
            self.update_context(response_content)
            print("\n\nNext one: \n\n")
            print(response_content)
            self.monitor.publish(objective="Fetched Image analysis...", module="LOG (ImageProcessor)")
        except Exception as e:
            print(f"Error during image analysis: {e}")

    def update_context(self, text):
        if not self.image_data.set_context(text):
            raise Exception("Failed to update the context.")

# if __name__ == "__main__":
#     image_data = ImageData("../../TestData/download.jpeg", event_id=123, serial_id=456)
#     processor = ImageProcessor(api_key="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")
#     processor.fetch_image_analysis(image_data)
#     print(image_data.get_context())

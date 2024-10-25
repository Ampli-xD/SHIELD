from groq import Groq


class AudioProcessor:
    def __init__(self, api_key):
        self.audio_data = None
        self.client = Groq(api_key=api_key)

    def fetch_audio_transcription(self, audio_data_object, model="whisper-large-v3-turbo", prompt="", language="en",
                                  temperature=0.0):
        self.audio_data = audio_data_object
        try:
            transcription = self.client.audio.transcriptions.create(
                file=self.audio_data.audio_path,
                model=model,
                prompt=prompt,
                response_format="verbose_json",
                language=language,
                temperature=temperature,
                timeout=1000
            )
            response_text = transcription.text
            self.update_context(response_text)

        except Exception as e:
            print(f"Error during audio transcription: {e}")

    def update_context(self, text):
        if not self.audio_data.set_context(text):
            raise Exception("Failed to update the context.")

# if __name__ == "__main__":
#     audio_data = AudioData(audio_path=os.path.join(os.path.dirname(__file__), "sample_audio.m4a"), event_id=123, serial_id=456)
#     processor = AudioProcessor(api_key="your_api_key_here")
#     processor.fetch_audio_transcription(audio_data)
#     print(audio_data.get_context())

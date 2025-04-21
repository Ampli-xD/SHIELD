import json

from groq import Groq


class LLMGenerator:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)

    def score_text_by_llm(self, user_message, model="llama-3.3-70b-versatile", system_prompt="",
                      temperature=0.8, max_tokens=340, top_p=1, stop=None, stream=False):
        try:
            # Create the chat completion request
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                stop=stop,
                stream=stream
            )
            # Extract the generated text
            response_text = chat_completion.choices[0].message.content
            json_format = json.loads(response_text)
            return json_format

        except Exception as e:
            print(f"Error during text generation: {e}")
            return None

# Example usage
# if __name__ == "__main__":
#     text_generator = TextGenerator(api_key="your_api_key_here")
#     user_message = "Explain the importance of fast language models"
#     generated_text = text_generator.generate_text(user_message)
#     if generated_text:
#         print("Generated Text:", generated_text)

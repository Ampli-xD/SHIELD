from groq import Groq

from Engine.LLMHandler.LLMPrompt import Prompt


class LLMGenerator:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)

    def generate_text(self, user_message, model="llama3-8b-8192", system_prompt=Prompt,
                      temperature=0.8, max_tokens=2000, top_p=1, stop=None, stream=False):
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
            return response_text

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

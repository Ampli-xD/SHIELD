import base64

from groq import Groq


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


# Path to your image
image_path = "../../Tests/TestData/download.jpeg"

# Getting the base64 string
base64_image = encode_image(image_path)

client = Groq(api_key="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")

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text",
                 "text": "Elaborate this scene in depth without missing any details and dont add assumptions to it just explain the scene, also tell if there is any text in the image"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                },
            ],
        }
    ],
    model="llama-3.2-11b-vision-preview",
)

print(chat_completion.choices[0].message.content)

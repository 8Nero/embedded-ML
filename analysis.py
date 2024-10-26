import base64
import sys

from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

prompt = """
    The following image was captured during a person detection event. 
    Analyze the image and provide a detailed report on the detected individuals."""

def analyze_image(image_path):
    # Prepare the prompt
    base64_image = encode_image(image_path)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        model="llava-v1.5-7b-4096-preview",
    )
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    print(analyze_image(sys.argv[1]))
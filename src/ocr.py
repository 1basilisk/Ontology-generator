# === src/ocr_engine.py ===
import base64
import io
import os
from PIL import Image
from dotenv import load_dotenv
from groq import Groq   


def encode_image_to_base64(image_path):
    with Image.open(image_path) as img:
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

def extract_text_from_image(image_path):
    encoded_image = encode_image_to_base64(image_path)

    load_dotenv()
    client = Groq()
    prompt = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "you are an ai assistant and your job is to extract all readable text from the image and return it as a string."
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "\n"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}"
                        }
                    },
                    {
                        "type": "text",
                        "text": "\n"
                    }
                ]
            }
        ]
    
    messages = prompt
    completion = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL"),
        messages=messages,
        max_tokens=5000,
        temperature=0.5,
        top_p=0.9,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False)
    

    return completion.choices[0].message.content.strip()


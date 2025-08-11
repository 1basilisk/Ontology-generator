import base64
import io
import os
from PIL import Image
from dotenv import load_dotenv
from groq import Groq, GroqError
import logging
from src.responseLogger import logResponse


load_dotenv()
client = Groq()

def encode_image_to_base64(image_path):
    with Image.open(image_path) as img:
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

def extract_text_from_image(image_path):
    encoded_image = encode_image_to_base64(image_path)


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
    try:
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
        
        logResponse({
            "status": "success",
            "headers": dict(completion.headers) if hasattr(completion, "headers") else None,
            "output": completion.choices[0].message.content.strip(),
            "image_path": image_path
        })
        
        return completion.choices[0].message.content.strip()
        
    except GroqError as e:
        error_info = str(e)
        headers = getattr(e, "headers", None)
        logResponse({
            "status": "groq_error",
            "error": error_info,
            "headers": dict(headers) if headers else None,
            "image_path": image_path
        })

        if any(word in error_info.lower() for word in ["quota", "exceeded", "limit"]):
            print("⚠️ Quota exhausted")
            logging.error("⚠️ Quota exhausted\n")
            return ""

    except Exception as e:
        error_info = str(e)
        logResponse({
            "status": "exception",
            "error": error_info,
            "headers": None,
            "image_path": image_path
        })

        print(f"Error connecting to LLM: {error_info}")
        logging.error(f"Error connecting to LLM: {error_info}\n")
        return ""
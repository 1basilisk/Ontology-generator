import os
import logging
import io
from PIL import Image
from dotenv import load_dotenv
from google import genai
from google.genai import types
from src.responseLogger import logResponse

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def encode_image_to_bytes(image_path):
    """Read image and return raw bytes."""
    with Image.open(image_path) as img:
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()

def extract_text_from_image(image_path: str) -> str:
    try:
        image_bytes = encode_image_to_bytes(image_path)

        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-1.5-pro"),
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
                "You are an AI assistant. Extract all readable text from this image and return only the text as plain output."
            ],
            config=types.GenerateContentConfig(
                temperature=0.5,
                top_p=0.9,
                max_output_tokens=5000
            )
        )

        text = response.text.strip()
        logResponse({
            "status": "success",
            "model": os.getenv("GEMINI_MODEL"),
            "output": text,
            "image_path": image_path
        })
        return text

    except Exception as e:
        err = str(e)
        logging.error(f"Gemini OCR error: {err}")
        logResponse({
            "status": "gemini_error",
            "model": os.getenv("GEMINI_MODEL"),
            "error": err,
            "image_path": image_path
        })
        return ""

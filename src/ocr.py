import os
import logging
import io
import base64
from PIL import Image
from dotenv import load_dotenv
from google import genai
from google.genai import types
from src.responseLogger import logResponse

# Load environment variables
load_dotenv()

# Initialize Gemini API client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def encode_image_to_bytes(image_path):
    """Read an image file and return bytes."""
    with Image.open(image_path) as img:
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        return buffered.getvalue()

def extract_text_from_image(image_path):
    """Extract text from image using Google Gemini Vision API."""
    try:
        image_bytes = encode_image_to_bytes(image_path)

        # Call Gemini API with image + instruction
        completion = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-1.5-pro"),
            contents=[
                types.ImageMessage(content=image_bytes),
                "You are an AI assistant. Extract all readable text from the image and return only the text as plain string."
            ],
            config=types.GenerateContentConfig(
                temperature=0.5,
                top_p=0.9,
                max_output_tokens=5000
            )
        )

        text_output = completion.text.strip()

        logResponse({
            "status": "success",
            "headers": None,  # Gemini SDK doesn't expose HTTP headers
            "output": text_output,
            "image_path": image_path
        })

        return text_output

    except Exception as e:
        error_info = str(e)
        logResponse({
            "status": "gemini_error",
            "error": error_info,
            "headers": None,
            "image_path": image_path
        })

        if any(word in error_info.lower() for word in ["quota", "exceeded", "limit"]):
            print("⚠️ Quota exhausted")
            logging.error("⚠️ Quota exhausted\n")
            return ""

        print(f"Error connecting to Gemini: {error_info}")
        logging.error(f"Error connecting to Gemini: {error_info}\n")
        return ""

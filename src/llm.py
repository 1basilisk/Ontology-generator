import os
import logging
from dotenv import load_dotenv
from google import genai
from google.genai import types
from src.responseLogger import logResponse

load_dotenv()


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# If you want to use Vertex AI instead, uncomment and configure:
# client = genai.Client(vertexai=True, project="your-gcp-project", location="us-central1")


def run_llm(prompt: str) -> str:
    """
    Sends prompt to Gemini model and returns output text.
    Logs full response or any errors.
    """
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=[prompt],
            config=types.GenerateContentConfig(
                temperature=0.5,
                top_p=0.9,
                max_output_tokens=5000
            )
        )
        text = response.text.strip()

        logResponse({
            "status": "success",
            "model": model_name,
            "response": text
        })
        return text

    except Exception as e:
        error_str = str(e)
        logging.error(f"Gemini API error: {error_str}")
        logResponse({
            "status": "gemini_error",
            "model": model_name,
            "error": error_str
        })
        return ""

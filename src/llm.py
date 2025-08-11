from groq import Groq, GroqError
import os
from dotenv import load_dotenv
import logging
from src.responseLogger import logResponse

load_dotenv()
client = Groq()

def generate_ontology_fragment(prompt):

    try:
        response = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL"),
            messages=[{"role": "user", "content": prompt}],
            max_tokens=5000,
            temperature=0.5,
            top_p=0.9,
            frequency_penalty=0,
            presence_penalty=0
        )
        logResponse({
            "status": "success",
            "headers": dict(response.headers) if hasattr(response, "headers") else None,
            "output": response.choices[0].message.content.strip()
        })

    except GroqError as e:
        error_info = str(e)
        headers = getattr(e, "headers", None)
        logResponse({
            "status": "groq_error",
            "error": error_info,
            "headers": dict(headers) if headers else None,
        })

        if "quota" in str(e).lower() or "exceeded" in str(e).lower() or "limit" in str(e).lower():
            print("⚠️ Quota exhausted")
            logging.error("⚠️ Quota exhausted\n")
            return ""
        

    except Exception as e:
        error_info = str(e)
        headers = getattr(e, "headers", None)
        logResponse({
            "status": "exception",
            "error": error_info,
            "headers": dict(headers) if headers else None,
        })

        print(f"Error generating ontology fragment: {e}")
        logging.error(f"Error generating ontology fragment: {e}\n")
        return ""
    return response.choices[0].message.content.strip()


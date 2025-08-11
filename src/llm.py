from groq import Groq, GroqError
import os
from dotenv import load_dotenv
import logging

def generate_ontology_fragment(prompt):
    load_dotenv()
    client = Groq()

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
    except GroqError as e:
        if "quota" in str(e).lower() or "exceeded" in str(e).lower() or "limit" in str(e).lower():
            print("⚠️ Quota exhausted")
            logging.error("⚠️ Quota exhausted\n")
            return ""
        

    except Exception as e:
        print(f"Error generating ontology fragment: {e}")
        logging.error(f"Error generating ontology fragment: {e}\n")
        return ""
    return response.choices[0].message.content.strip()


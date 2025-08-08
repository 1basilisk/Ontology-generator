from groq import Groq
import os

def generate_ontology_fragment(prompt):
    client = Groq()
    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL"),
        messages=[{"role": "user", "content": prompt}],
        max_tokens=5000,
        temperature=0.5,
        top_p=0.9,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message.content.strip()


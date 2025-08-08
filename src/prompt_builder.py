def build_prompt(text_chunk, current_ontology_ttl):
    return f"""
You are an ontology engineer. Convert the following text into an OWL ontology fragment using Turtle syntax.

TEXT:
"{text_chunk}"

CURRENT ONTOLOGY:
{current_ontology_ttl}

TASK:
Your task is to generate a turtle fragment that represents the concepts, relationships, and properties described in the text. Ensure that the fragment is consistent with the current ontology.
Make sure to use appropriate prefixes and URIs for the ontology elements. The fragment should be valid Turtle syntax and should not include any extraneous information.
Return only the Turtle fragment without any additional explanations or comments. directly return the Turtle fragment as a string. do not use any markers like ```turtle or ```json etc.
"""
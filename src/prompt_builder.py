def build_generation_prompt(text_chunk):
    return f"""
You are an ontology engineer. Convert the following text into an OWL ontology fragment using Turtle syntax.

TEXT:
"{text_chunk}"

TASK:
Your task is to generate a turtle fragment that represents the concepts, relationships, and properties described in the text. Ensure that the fragment is consistent with the current ontology.
Make sure to use appropriate prefixes and URIs for the ontology elements. The fragment should be valid Turtle syntax and should not include any extraneous information.
Return only the Turtle fragment without any additional explanations or comments. directly return the Turtle fragment as a string. do not use any markers like ```turtle or ```json etc.

make sure there are no syntax errors in output. here is an example ontology for reference:
@prefix ns1: <http://example.org/ontology#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ns1:Person a rdfs:Class .
ns1:Doctor a rdfs:Class .
ns1:hasDoctor a rdf:Property ;
    rdfs:domain ns1:Person ;
    rdfs:range ns1:Doctor .

ns1:hasName a rdf:Property ;
    rdfs:domain ns1:Person ;
    rdfs:range xsd:string .

IMPORTANT  Common Mistakes to Avoid:
1. Vocabulary:
   - Do NOT create duplicate classes or properties with slightly different names (e.g., Doctor vs Doctors).
   - Use consistent naming style (PascalCase for classes, camelCase for properties).
   - Avoid overly generic names like Entity, Object, or Thing.

2. Structure:
   - Always define @prefix declarations for all namespaces you use.
   - Ensure domains and ranges are logically correct (e.g., hasName should apply to a Person, not a Treatment).
   - Use owl:ObjectProperty for links between entities; use owl:DatatypeProperty for literal values.
   - Do NOT declare individuals as classes or classes as individuals.

3. Semantics:
   - Maintain correct class hierarchies; avoid illogical subclass relationships.
   - Avoid contradictory axioms (e.g., a class cannot be both equivalent and disjoint).
   - Add labels and rdfs:comment to make ontology human-readable.

4. Syntax:
   - Ensure valid Turtle syntax (proper periods, no dangling triples).
   - URIs must be valid (no spaces or illegal characters).
   - Do not reference undefined classes or properties.

5. Scope:
   - Only model concepts clearly described in the input text.
   - Avoid over-generalizing or adding unrelated concepts.

"""

def build_validation_prompt(ontology):
    return f"""
        You are an ontology validator. Review the following OWL ontology in Turtle format.

        TASK:
        1. Fix any syntax errors so it is valid Turtle.
        2. Merge duplicate classes or properties with different names but identical meaning.
        3. Ensure consistent naming (PascalCase for classes, camelCase for properties).
        4. Remove any undefined references.
        5. Ensure all object properties have correct domain/range.
        6. Do not add any new classes or properties that are not present in the original ontology.

        Return ONLY the corrected Turtle format. Do not add explanations or comments. directly return the Turtle fragment as a string. do not use any markers like ```turtle or ```json etc.

        ONTOLOGY:
        {ontology}
    """

def build_repair_fragment_prompt(turtle_str):
    return f"""
        You are an expert in OWL ontologies and Turtle syntax.
        The following Turtle fragment has syntax errors that prevent parsing.

        TASK:
        - Fix the syntax so it is valid Turtle.
        - Keep all triples exactly the same unless fixing syntax errors.
        - Do not add any unrelated content.
        - Do not change the ontology semantics.
        - Use proper prefixes.
        - Return only the fixed Turtle fragment, no explanations or formatting.

        Return ONLY the corrected Turtle format. Do not add explanations or comments. directly return the Turtle fragment as a string. do not use any markers like ```turtle or ```json etc.

        FRAGMENT:
        {turtle_str}
    """
    

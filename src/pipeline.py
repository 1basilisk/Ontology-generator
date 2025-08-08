from src.document_loader import load_documents
from src.ocr import extract_text_from_image
from src.splitter import split_text
from src.prompt_builder import build_prompt
from src.llm import generate_ontology_fragment
from src.ontology_builder import OntologyBuilder
import os


def run_pipeline():
    doc_paths = load_documents("data/raw")
    BASE_URI = os.getenv("BASE_URI", "http://example.com/ontology")
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
    ob = OntologyBuilder(BASE_URI)

    for doc_path in doc_paths:
        if doc_path.endswith(('.png', '.jpg', '.jpeg')):
            text = extract_text_from_image(doc_path)
            
            text_filename = f"data/processed/{os.path.splitext(os.path.basename(doc_path))[0]}.txt"
            
            with open(text_filename, "w", encoding="utf-8") as text_file:
                text_file.write(text)

        else:
            with open(doc_path, 'r', encoding='utf-8') as f:
                text = f.read()

        chunks = split_text(text, CHUNK_SIZE)

        for chunk in chunks:
            prompt = build_prompt(chunk, ob.get_current_ontology_ttl())
            fragment = generate_ontology_fragment(prompt)

            fragment_filename = f"data/ontology_fragments/{os.path.basename(doc_path)}_{chunks.index(chunk)}.ttl"
            with open(fragment_filename, "w", encoding="utf-8") as frag_file:
                frag_file.write(fragment)

            ob.merge_fragment(fragment)

    ob.save_to_file("output/final_ontology.ttl")
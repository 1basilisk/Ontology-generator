from src.document_loader import load_documents
from src.ocr import extract_text_from_image
from src.splitter import split_text
from src.prompt_builder import build_prompt
from src.llm import generate_ontology_fragment
from src.ontology_builder import OntologyBuilder
import os
import time
import logging


def run_pipeline():
    
        
    logging.info("Starting ontology generation pipeline")
    doc_paths = load_documents("data/processed")
    BASE_URI = os.getenv("BASE_URI", "http://example.com/ontology")
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
    ob = OntologyBuilder(BASE_URI)

    for doc_path in doc_paths:
        if doc_path.endswith(('.png', '.jpg', '.jpeg')):
            text = extract_text_from_image(doc_path)
            if not text:
                print(f"No text extracted from {doc_path}. Skipping.")
                logging.info(f"No text extracted from {doc_path}. Skipping.\n")
                continue
            print(f"Extracted text from {doc_path}.")
            logging.info(f"Extracted text from {doc_path}.\n")
            
            text_filename = f"data/processed/{os.path.splitext(os.path.basename(doc_path))[0]}.txt"
            
            with open(text_filename, "w", encoding="utf-8") as text_file:
                text_file.write(text)
                print(f"Text saved to {text_filename}")     
                logging.info(f"Text saved to {text_filename}\n")


        else:
            with open(doc_path, 'r', encoding='utf-8') as f:
                text = f.read()

        chunks = split_text(text, CHUNK_SIZE)
        print(f"Processing {len(chunks)} chunks from {doc_path}.")
        logging.info(f"Processing {len(chunks)} chunks from {doc_path}.\n")

        for i, chunk in enumerate(chunks):
            prompt = build_prompt(chunk, ob.get_current_ontology_ttl())
            fragment = generate_ontology_fragment(prompt)
            print(f"Generated fragment for chunk: {i}")  
            logging.info(f"Generated fragment for chunk: {i}\n")
            
            # print("waiting for 60 seconds before processing the next chunk...")
            # time.sleep(60)


            fragment_filename = f"data/ontology_fragments/{os.path.basename(doc_path)}_{chunks.index(chunk)}.ttl"
            with open(fragment_filename, "w", encoding="utf-8") as frag_file:
                frag_file.write(fragment)
            print(f"Fragment saved to {fragment_filename}")


            mergeSuccess = ob.merge_fragment(fragment)
            if not mergeSuccess:
                print(f"fragment {fragment_filename} did not merge due to error")
                logging.error(f"fragment {fragment_filename} did not merge due to error\n")

    ob.save_to_file("output/final_ontology.ttl")
    logging.info("Ontology generation pipeline completed successfully.\n")
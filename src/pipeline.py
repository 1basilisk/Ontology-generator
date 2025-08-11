from src.document_loader import load_documents
from src.ocr import extract_text_from_image
from src.splitter import split_text
from src.prompt_builder import build_prompt
from src.llm import generate_ontology_fragment
from src.ontology_builder import OntologyBuilder
import os
import time
import logging
from src.pdfProcessor import convert_pdf_to_images
import shutil

def run_pipeline(skip_raw=False, skip_ocr=False):
    logging.info("Starting ontology generation pipeline")
    doc_paths_raw = load_documents("data/raw") if not skip_raw else []
    images_dir = "data/images" 

    doc_paths_processed = load_documents("data/processed")
    BASE_URI = os.getenv("BASE_URI", "http://example.com/ontology")
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
    ob = OntologyBuilder(BASE_URI)

    #converting pdf to images and copying images to data/images
    for doc_path in doc_paths_raw:
        if doc_path.endswith('.pdf'):
            print(f"Processing PDF document: {doc_path}")
            logging.info(f"Processing PDF document: {doc_path}\n")
            convert_pdf_to_images(doc_path)
            print(f"Converted {doc_path} to images.")
        
        elif doc_path.endswith(('.png', '.jpg', '.jpeg')):
            
            os.makedirs(images_dir, exist_ok=True)
            dest_path = os.path.join(images_dir, os.path.basename(doc_path))
            shutil.copy(doc_path, dest_path)
            print(f"Copied {doc_path} to {dest_path}")
            logging.info(f"Copied {doc_path} to {dest_path}\n")

        elif doc_path.endswith('.txt'):
            #move to processed folder
            processed_dir = "data/processed"
            os.makedirs(processed_dir, exist_ok=True)
            dest_path = os.path.join(processed_dir, os.path.basename(doc_path))
            shutil.copy(doc_path, dest_path)
            print(f"Copied {doc_path} to {dest_path}")
            logging.info(f"Copied {doc_path} to {dest_path}\n")
        else:
            print(f"Unsupported file type: {doc_path}. Skipping.")
            logging.info(f"Unsupported file type: {doc_path}. Skipping.\n")
            continue

    #running OCR on images
    for doc_path in load_documents(images_dir) if not skip_ocr else []:
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
            print(f"Unsupported file type for OCR: {doc_path}. Skipping.")
            logging.info(f"Unsupported file type for OCR: {doc_path}. Skipping.\n")
            continue

    #processing text files and generating ontology fragments
    for doc_path in doc_paths_processed: 
        if doc_path.endswith('.txt'):
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
                time.sleep(60)


                fragment_filename = f"data/ontology_fragments/{os.path.basename(doc_path)}_{chunks.index(chunk)}.ttl"
                with open(fragment_filename, "w", encoding="utf-8") as frag_file:
                    frag_file.write(fragment)
                print(f"Fragment saved to {fragment_filename}")


                mergeSuccess = ob.merge_fragment(fragment)
                if not mergeSuccess:
                    print(f"fragment {fragment_filename} did not merge due to error")
                    logging.error(f"fragment {fragment_filename} did not merge due to error\n")
        else:
            print(f"Unsupported file type for processing: {doc_path}. Skipping.")
            logging.info(f"Unsupported file type for processing: {doc_path}. Skipping.\n")
            continue

    ob.save_to_file("output/final_ontology.ttl")
    logging.info("Ontology generation pipeline completed successfully.\n")
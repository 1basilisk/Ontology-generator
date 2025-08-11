# Ontology Generation Pipeline

## Overview

This project automates the extraction of structured ontological knowledge from raw documents (PDFs, images, and text files) using OCR and LLMs, and builds an OWL ontology in Turtle format. It is designed for ontology engineers and researchers who want to convert unstructured data into machine-readable ontologies.

---

## Project Structure

```
.
├── .env
├── .gitignore
├── app.log
├── requirements.txt
├── run.py
├── data/
│   ├── images/
│   ├── ontology_fragments/
│   ├── processed/
│   └── raw/
├── logs/
│   ├── app.log
│   └── llm_responses.jsonl
├── output/
│   └── final_ontology.ttl
└── src/
    ├── __init__.py
    ├── document_loader.py
    ├── llm.py
    ├── ocr.py
    ├── ontology_builder.py
    ├── pdfProcessor.py
    ├── pipeline.py
    ├── prompt_builder.py
    ├── responseLogger.py
    ├── splitter.py
    └── __pycache__/
```

---

## Main Components

### 1. Entry Point

- **`run.py`**:  
  The main script. Parses command-line arguments, sets up logging, and starts the pipeline via `src.pipeline.run_pipeline`.

### 2. Pipeline

- **`src/pipeline.py`**:  
  Orchestrates the workflow:
  - Loads raw documents.
  - Converts PDFs to images.
  - Runs OCR on images.
  - Processes text files (including OCR output).
  - Splits text into manageable chunks.
  - Builds prompts and queries the LLM for ontology fragments.
  - Merges fragments into a single ontology.
  - Saves the final ontology.

### 3. Document Handling

- **`src/document_loader.py`**:  
  Loads file paths from a given directory.

- **`src/pdfProcessor.py`**:  
  Converts PDF files to images for OCR processing.

### 4. OCR

- **`src/ocr.py`**:  
  Encodes images to base64 and sends them to the Groq LLM for text extraction.

### 5. Text Splitting

- **`src/splitter.py`**:  
  Splits large text into smaller chunks for LLM processing.

### 6. Prompt Construction

- **`src/prompt_builder.py`**:  
  Builds detailed prompts for the LLM to generate ontology fragments.

### 7. LLM Interaction

- **`src/llm.py`**:  
  Handles communication with the Groq LLM API, including error handling and logging.

### 8. Ontology Building

- **`src/ontology_builder.py`**:  
  Merges Turtle fragments into an RDFLib graph and serializes the final ontology.

### 9. Logging

- **`src/responseLogger.py`**:  
  Logs LLM responses and errors to `logs/llm_responses.jsonl`.

---

## Data Folders

- **`data/raw`**: Place your input documents (PDF, images, text) here.
- **`data/images`**: Intermediate storage for images (from PDFs or direct).
- **`data/processed`**: Stores processed text files (from OCR or direct).
- **`data/ontology_fragments`**: Stores generated ontology fragments for each chunk.
- **`output/final_ontology.ttl`**: The final merged ontology in Turtle format.

---

## Configuration

- **`.env`**:  
  Set your API keys and parameters here:
  ```
  GROQ_API_KEY="your_groq_api_key"
  GROQ_MODEL="openai/gpt-oss-120b"
  BASE_URI="http://example.com/ontology"
  CHUNK_SIZE=1000
  ```

---

## Usage

### 1. Install Dependencies

```sh
pip install -r requirements.txt
```

### 2. Prepare Data

- Place your raw documents in `data/raw`.

### 3. Run the Pipeline

```sh
python run.py
```

#### Optional Arguments

- `--skip-raw`: Skip processing of raw documents (PDF/image copying, etc.).
- `--skip-ocr`: Skip OCR on images (useful if you already have processed text).

Example:

```sh
python run.py --skip-raw --skip-ocr
```

---

## Output

- **Ontology Fragments**:  
  Each processed chunk produces a `.ttl` file in `data/ontology_fragments`.

- **Final Ontology**:  
  The merged ontology is saved as `output/final_ontology.ttl`.

- **Logs**:  
  - Application logs: `logs/app.log`
  - LLM responses: `logs/llm_responses.jsonl`

---

## Troubleshooting

- **Stuck or Slow Processing**:  
  - Each chunk waits 60 seconds before the next LLM call (see `time.sleep(60)` in `src/pipeline.py`).
  - LLM API/network issues can cause delays.
  - Check `logs/app.log` and `logs/llm_responses.jsonl` for errors.

- **Quota/Connection Errors**:  
  - See error messages in logs.
  - Ensure your `.env` has a valid `GROQ_API_KEY`.

---

## Extending

- Add new document types by extending `src/document_loader.py` and update the pipeline logic.
- Adjust prompt engineering in `src/prompt_builder.py` for different ontology extraction tasks.
- Change ontology serialization by modifying `src/ontology_builder.py`.

---

## License

This project is for educational and research purposes.  
Please ensure you comply with the terms of the Groq API and any other third-party services used.

---

## Authors

- Utkarsh Sharma

---

For more details, see the code in each module:
- `src/pipeline.py`
- `src/llm.py`
- `src/ocr.py`
- `src/ontology_builder.py`
- `src/prompt_builder.py`
- `src/splitter.py`
- `src/document_loader.py`
- `src/responseLogger.py
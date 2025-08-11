import os
import logging
import argparse
from src.pipeline import run_pipeline

if __name__ == "__main__":
    # --- Parse command-line args ---
    parser = argparse.ArgumentParser(description="Run the ontology pipeline")
    parser.add_argument("--skip-raw", action="store_true", help="Skip processing of raw documents")
    parser.add_argument("--skip-ocr", action="store_true", help="Skip OCR on images")
    args = parser.parse_args()

    # --- Ensure logs folder exists ---
    os.makedirs("logs", exist_ok=True)

    # --- Configure logging ---
    logging.basicConfig(
        filename="logs/app.log",
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )

    logging.info(f"Pipeline started (skip_raw={args.skip_raw}, skip_ocr={args.skip_ocr})")

    # --- Run pipeline with args ---
    run_pipeline(skip_raw=args.skip_raw, skip_ocr=args.skip_ocr)
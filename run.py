from src.pipeline import run_pipeline
import logging

if __name__ == "__main__":
    logging.basicConfig(
    filename="app.log",           # Log file path
    filemode="a",                 # Append mode ("w" to overwrite)
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO            # Logging level
)
    run_pipeline()

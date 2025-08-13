import json
import os
import time

def logResponse(data, filename="logs/llm_responses.jsonl"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    data["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")

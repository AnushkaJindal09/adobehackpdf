import os
import json
from heading_extractor import extract_headings_from_pdf

INPUT_DIR = "./input"
OUTPUT_DIR = "./output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

for filename in os.listdir(INPUT_DIR):
    if filename.lower().endswith(".pdf"):
        path = os.path.join(INPUT_DIR, filename)
        print(f" {filename}")
        try:
            result = extract_headings_from_pdf(path)
            with open(os.path.join(OUTPUT_DIR, filename.replace(".pdf", ".json")), "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(" Extracted")
        except Exception as e:
            print(f" Failed — {e}")

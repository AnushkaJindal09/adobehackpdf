import os
import json
from datetime import datetime
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer

from outline_extractor import extract_headings_from_pdf
from relevance_ranker import rank_headings_by_relevance
from auto_task_detector import detect_task

INPUT_DIR = "input"
OUTPUT_DIR = "output"
model = SentenceTransformer("all-MiniLM-L6-v2")


persona, job = detect_task(INPUT_DIR)
query = f"{persona}. Task: {job}"


metadata = {
    "input_documents": [],
    "persona": persona,
    "job_to_be_done": job,
    "processing_timestamp": datetime.now().isoformat()
}

extracted_sections = []
refined_subsections = []


def is_valid_title(title):
    title_clean = title.strip().lower()
    return (
        len(title_clean) > 3 and
        not title_clean.isnumeric() and
        title_clean not in {
            '', 'of', 'the', 'and', 'page', 'a', 'an',
            'contents', 'certificate', 'official journal', 'publication of the patent office'
        }
    )


def extract_full_section_text(pdf_path, start_page, current_title, stop_titles):
    try:
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        collected_text = []
        stop_titles_lower = [s.strip().lower() for s in stop_titles if is_valid_title(s)]

        for i in range(start_page - 1, total_pages):
            page_text = reader.pages[i].extract_text()
            if not page_text:
                continue

            lines = page_text.split("\n")
            for line in lines:
                stripped = line.strip().lower()
                # Stop if next valid heading appears
                if stripped in stop_titles_lower and stripped != current_title.strip().lower():
                    return "\n".join(collected_text).strip()
                collected_text.append(line)

        return "\n".join(collected_text).strip()
    except Exception as e:
        return f"(Error extracting section: {e})"


for file in os.listdir(INPUT_DIR):
    if file.endswith(".pdf"):
        pdf_path = os.path.join(INPUT_DIR, file)
        metadata["input_documents"].append(file)

        try:
            #  Use 1A-style heading extractor
            outline_result = extract_headings_from_pdf(pdf_path)
            title = outline_result["title"]
            outline = outline_result["outline"]


            cleaned_outline = [item for item in outline if is_valid_title(item["text"])]
            ranked = rank_headings_by_relevance(cleaned_outline, query, model)
            titles_in_doc = [item["text"].strip() for item in cleaned_outline]

            for i, item in enumerate(ranked[:10]):
                section_title = item["text"]
                page_number = item["page"]

                extracted_sections.append({
                    "document": file,
                    "section_title": section_title,
                    "importance_rank": i + 1,
                    "page_number": page_number
                    
                })

                #  Extract full section text
                stop_titles = titles_in_doc[titles_in_doc.index(section_title) + 1:]
                refined_text = extract_full_section_text(pdf_path, page_number, section_title, stop_titles)

                refined_subsections.append({
                    "document": file,
                    "refined_text": refined_text if refined_text else "(No content found)",
                    "page_number": page_number,
                    "section_title": section_title
                    
                })

        except Exception as e:
            print(f"[!] Error processing {file}: {e}")

#  Final JSON Output
final_output = {
    "metadata": metadata,
    "extracted_sections": extracted_sections,
    "subsection_analysis": refined_subsections
}

os.makedirs(OUTPUT_DIR, exist_ok=True)
out_path = os.path.join(OUTPUT_DIR, "SOP_IST.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(final_output, f, indent=2)

print(f"✅ Extraction complete. Output written to {out_path}")

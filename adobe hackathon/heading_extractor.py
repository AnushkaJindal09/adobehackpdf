import fitz
import re
from langdetect import detect
from collections import defaultdict

def is_heading_candidate(text):
    if not text or len(text.strip()) < 3:
        return False
    if len(text.split()) > 12:
        return False
    if text.replace(" ", "").isdigit():
        return False
    if text.startswith(("•", "●", "-", "*")):
        return False
    if text.lower() in {"yes", "no", "and", "the", "at", "on"}:
        return False
    return True

def score_heading(text, size, is_bold, alignment):
    score = 0
    try:
        lang = detect(text)
        if lang not in ['en', 'hi', 'mr', 'bn', 'ta', 'te', 'gu', 'kn', 'ja', 'ko', 'zh-cn', 'zh-tw', 'fr', 'es', 'de', 'it', 'pt', 'ru', 'ar', 'fa', 'tr']:
            score -= 1
    except:
        score -= 1

    if is_bold:
        score += 2
    if size >= 14:
        score += 2
    if alignment == "center":
        score += 1
    if text.isupper():
        score += 1
    if text.endswith(":"):
        score += 1
    if re.match(r"^[0-9]+(\.[0-9]+)*\s", text):
        score += 2
    if len(text.split()) <= 6:
        score += 2  

    return score

def extract_headings_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    spans_info = []
    font_sizes = defaultdict(int)

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                line_text = " ".join(span["text"].strip() for span in line["spans"])
                if not is_heading_candidate(line_text):
                    continue
                first_span = line["spans"][0]
                size = round(first_span["size"], 1)
                font = first_span["font"]
                flags = first_span["flags"]
                is_bold = flags & 2 != 0 or "Bold" in font
                x0 = first_span["bbox"][0]
                alignment = "center" if 180 < x0 < 420 else "left"
                score = score_heading(line_text, size, is_bold, alignment)

                spans_info.append({
                    "text": line_text,
                    "size": size,
                    "is_bold": is_bold,
                    "alignment": alignment,
                    "page": page_num,
                    "score": score
                })

                font_sizes[size] += 1

    
    top_sizes = [fs[0] for fs in sorted(font_sizes.items(), key=lambda x: -x[1])[:3]]
    size_to_level = {}
    if len(top_sizes) >= 1: size_to_level[top_sizes[0]] = "H1"
    if len(top_sizes) >= 2: size_to_level[top_sizes[1]] = "H2"
    if len(top_sizes) >= 3: size_to_level[top_sizes[2]] = "H3"

    seen = set()
    outline = []
    for span in spans_info:
        text = span["text"]
        if text in seen or span["score"] < 3: 
            continue
        seen.add(text)
        level = size_to_level.get(span["size"], "H3")
        outline.append({
            "text": text.rstrip(":"),
            "level": level,
            "page": span["page"]
        })

    
    title = None
    if top_sizes:
        for span in spans_info:
            if span["page"] == 1 and span["size"] == top_sizes[0]:
                title = span["text"]
                break
    if not title:
        title = "Untitled Document"

    return {
        "title": title,
        "outline": outline
    }


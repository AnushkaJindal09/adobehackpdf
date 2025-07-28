# Challenge 1B: Persona-Driven Document Intelligence

## Problem Overview

Today’s world is overloaded with information — yet what professionals actually need is *insight*. Whether it’s a student cramming for exams, a researcher writing a review, or an analyst summarizing financials, most users don’t have the time to manually browse long, unstructured PDFs.

**Challenge 1B** reimagines document intelligence by focusing on:
- *Who* the reader is (Persona)
- *Why* they’re reading (Job to be done)
- *What* matters most (Relevant content, not just headings)

---

## Objective

Build an intelligent document analysis system that:
1. Accepts a folder of 3–10 unstructured PDF files
2. Automatically detects the user's **persona** and their **goal**
3. Extracts and ranks the **most relevant sections** with actual content

This system should act like a research assistant — highlighting what matters, skipping the fluff, and working offline.

---

## Performance & Constraints

- CPU-only execution (No GPU)
- Runs completely offline (no internet calls)
- Model size under 1GB (uses `all-MiniLM-L6-v2`)
- Processes 3–5 PDFs in under 60 seconds


## Key Features

### 1. Auto Persona & Task Identification
- No manual config — the system inspects documents to infer:
  - The likely **persona** (e.g., PhD Student, Salesperson)
  - The associated **job-to-be-done** (e.g., Literature Review, Sales Prep)

- Example cues:
  - Phrases like "exam tips", "syllabus", or "reaction mechanisms" → Student  
  - Mentions of "market share", "strategy", "investment trends" → Analyst  

### 2. Semantic Section Ranking
- Uses a combination of:
  - SentenceTransformers (`all-MiniLM-L6-v2`)
  - Cosine similarity on section titles
  - Smart filtering of noisy or generic headings

- Outputs the **Top 10** most relevant sections, sorted by importance.

### 3. Real Subsection Text Extraction
- Goes beyond section titles — this system extracts:
  - Full **section content**, spanning multiple pages if needed  
  - Stops intelligently at the next relevant heading  
  - Ensures the output is *usable*, *insightful*, and *non-generic*

### 4. Noise Filtering & Clean Structuring
- Filters out:
  - One-word headings like “OF”, “AND”, “PAGE”
  - Blank or numeric-only titles
  - Non-content sections like "Table of Contents" or "Certificate"

---

## Input & Output

### Input
- A folder called `input/` containing 3–10 PDF documents (any domain)

### Output
- A single structured JSON file: `output/SOP_IST.json`, with:
  - `metadata`: persona, job, input files, timestamp
  - `extracted_sections`: Top relevant sections (title, page, rank)
  - `subsection_analysis`: Real text from those sections

---

## Why It Works

This system doesn’t rely on hand-tuned rules or hardcoded logic. It adapts on the fly to:
- Academic PDFs
- Annual reports
- News articles
- Legal documents
- Chemistry textbooks

All offline, with no internet dependency.

---

## Stack & Tools

| Tool / Library         | Purpose                                               |
|------------------------|-------------------------------------------------------|
| Python 3.10+           | Core scripting language                               |
| PyPDF2                 | Page-level text extraction                            |
| pymupdf (fitz)         | Heading detection using font size, boldness, layout   |
| SentenceTransformers   | Semantic embedding of section titles                  |
| scikit-learn           | Cosine similarity scoring for heading relevance       |
| torch                  | Backend support for sentence-transformers             |
| transformers           | Required by sentence-transformers for some operations |
| langdetect             | Multilingual support                                  |


---

## Directory Layout

round1b/
├──app/
│   ├── auto_task_detector.py       # Persona & job detection from text
│   ├── extract_relevant.py         # Core processing pipeline
│   ├── outline_extractor.py        # Reused from Round 1A (modular)
│   ├── relevance_ranker.py         # Ranks section titles by semantic similarity
│   ├── input/                      # Folder containing input PDFs
│   ├── output/                     # Output JSON gets saved here
│   └── __pycache__/                # Python cache (can ignore in Git)
├── approach_explanation.md         # 300-500 word explanation
├── Dockerfile                      # Offline container build
├── requirements.txt                # All required pip packages
└── README.md                       # This file



---

## How It Connects to Round 1A

This solution builds on the modular design from Round 1A:
- The `outline_extractor.py` from 1A is **reused** to get structured document outlines
- This ensures consistency and avoids code duplication
- Also complies with Adobe’s Round 1B guideline: *"Make your code modular — you’ll reuse this structure in Round 1B."*

---

## Strengths of Our Solution

-  **Fast** — Works within 60s for 3–5 documents
-  **Context-Aware** — Understands persona needs and adapts
-  **Scalable** — Works on education, finance, research, and more
-  **Offline-Ready** — Zero internet or API requirements
-  **Generalized** — No file-specific hacks or hardcoding

---

## Handling Edge Cases

- If an unknown persona is encountered, the system falls back to:
  - `"Curious Reader"` as a neutral default
  - Still returns relevant content using general semantic cues

- If heading structure is weak, fallback text analysis ensures extraction still works

---

## Output Sample (Trimmed)
```json
{
  "metadata": {
    "persona": "Undergraduate Student",
    "job_to_be_done": "Exam Preparation - Organic Chemistry",
    "input_documents": ["Chemistry_Chapter3.pdf"],
    "processing_timestamp": "2025-07-27T21:30:00Z"
  },
  "extracted_sections": [
    {
      "document": "Chemistry_Chapter3.pdf",
      "section_title": "Reaction Mechanisms",
      "page_number": 4,
      "importance_rank": 1
    },
    ...
  ],
  "subsection_analysis": [
    {
      "document": "Chemistry_Chapter3.pdf",
      "section_title": "Reaction Mechanisms",
      "page_number": 4,
      "refined_text": "This section discusses SN1 and SN2 mechanisms, including intermediate formation, stereochemistry, and rate-determining steps."
    },
    ...
  ]
}
```
Output is saved as a structured JSON file (output/SOP_IST.json) containing metadata, top-ranked sections, and real content analysis.


---

## Conclusion

This pipeline delivers real document intelligence — combining automation, context-awareness, and offline reliability. It's not just fast; it’s insightful, adaptable, and ready for any PDF challenge.

# Approach Explanation — Round 1B

## Problem Understanding

In today's digital workspace, professionals across industries deal with large, unstructured PDFs that are time-consuming to navigate. Whether it's a student looking for syllabus topics, an analyst scanning financial reports, or a researcher reviewing literature, the challenge remains the same — how to quickly extract *relevant* information based on *user context*.

The core problem lies in building a system that can do this automatically — **without internet access, without manual configuration**, and without relying on labeled training data. Our solution focuses on just that.

---

## System Overview

We designed a modular, zero-shot pipeline that works offline, on CPU, and is fully generalizable across personas and domains. It performs the following:

### 1. **Persona & Task Inference**

- The system analyzes the **first 2–3 pages** of each document using lightweight keyword-based logic.
- It automatically infers:
  - The **persona** (e.g., Undergraduate Student, Analyst, Researcher, Salesperson)
  - The **job-to-be-done** (e.g., Exam Prep, Literature Review, Benchmarking)

No manual `.json` or external metadata is required — everything is inferred from the documents.

---

### 2. **Outline Extraction & Cleanup**

- We use structural heuristics and `PyPDF2` to extract candidate **section titles**.
- These are filtered to remove:
  - Generic or non-informative labels like `PAGE`, `OF`, `:NA`
  - Short titles (< 4 characters) or numeric-only sections

This ensures only meaningful headings are passed on for ranking.

---

### 3. **Semantic Relevance Ranking**

- Each cleaned section heading is embedded using `SentenceTransformers` (`all-MiniLM-L6-v2`).
- Cosine similarity is computed between section embeddings and the persona–task prompt.
- The system selects the **Top 10** most relevant sections across all PDFs.

---

### 4. **Real Subsection Text Extraction**

- For each selected heading, the system extracts actual **page-level text**, not placeholders.
- Text is extracted intelligently (multi-page where needed) and stops at the next detected heading.
- This ensures that output is truly **usable and context-rich** for downstream tasks.

---

## Generalization & Offline Constraints

This system is built for constrained environments and general use:

-  **Runs Offline**: No internet or APIs needed  
-  **Model size < 100MB**  
-  **CPU-only**  
-  **3–5 PDFs processed under 60 seconds**

Unknown personas (e.g., “Policy Analyst” or “Doctor”) are handled by:
- Falling back to the most semantically similar known role  
- Or assigning a default `"Curious Reader"` persona  

---

## Reusability

The architecture is fully modular and aligns with Round 1A's philosophy:
- Each module (persona detection, relevance ranking, text extraction) is **decoupled and reusable**
- The same structure supports Round 2 enhancements, like integrating with UI tools (e.g., Adobe PDF Embed API)

---

## Summary

This solution builds a domain-agnostic, persona-aware document intelligence system — one that reads documents like a human would, but with the speed and consistency of a machine. It handles ambiguity, works offline, and delivers real insight tailored to the user's intent — all within the tight constraints of the challenge.

# Challenge 1a: PDF Heading Extraction Solution  
Adobe India Hackathon 2025

# Overview

This repository provides a complete solution for **Challenge 1A** of the Adobe India Hackathon 2025.  
The goal is to build a **PDF processing system** that extracts structured **document titles and headings** from PDF files and generates corresponding `.json` files for each input.  

The system works **offline, is multilingual**, and supports **both simple and complex PDFs**.


## Submission Components

-  **Dockerfile** in root directory
-  **Fully working source code** (`heading_extractor.py`, `main.py`)
-  **README.md** (you’re reading it)
-  Output adheres to schema provided in `sample_dataset/schema/output_schema.json`


##  Key Features

-  **Title and heading extraction** using PyMuPDF and intelligent heuristics
-  **Multilingual support** via `langdetect` (English, Hindi, Korean, Arabic, and more)
-  Supports both:
  - Simple documents with standard formatting
  - Complex flyers with visual layout structure
-  No internet, no cloud dependency — **fully offline and CPU-only**
-  Packaged using **Docker** for reproducibility and AMD64 compatibility


### Critical Constraints
 Fast Execution (≤ 10 Seconds for 50-Page PDF)
 Model-Free, Lightweight Architecture
 Offline, Air-Gapped Operation
 CPU-Only Runtime (8 CPUs / 16 GB RAM Compatible)
 AMD64 Architecture Compliance
 Flexible and Cross-PDF Compatible

# Folder Structure

ADOBE HACKATHON/
├── input/
│   └── .gitkeep             
├── output/
│   └── .gitkeep         
├── schema/
│   └── output_schema.json   
├── main.py              
├── heading_extractor.py 
├── requirements.txt     
├── Dockerfile           
└── Readme.md            

## How It Works

The extractor uses a mix of **font size**, **boldness**, **position**, **alignment**, and **language cues** to assign a **confidence score** to each text line.

- Font size drives H1/H2/H3 level classification
- Boldness, all-uppercase text, and alignment boost heading confidence
- Outputs structured `outline[]` with:
  - `text`: heading text
  - `level`: "H1", "H2", or "H3"
  - `page`: page number


##  Build & Run Instructions

### Build Docker Image
 docker build --platform=linux/amd64 -t heading-extractor-final .

### Run
docker run --rm --platform=linux/amd64 -v ${PWD}/input:/app/input -v ${PWD}/output:/app/output heading-extractor-final

### Final Checklist
- Docker image builds on linux/amd64
- Docker container runs with CPU only
- JSON output matches schema
- Input/output folders mapped correctly
- README includes all instructions
- Runs within time and memory limits
-  All required files are committed



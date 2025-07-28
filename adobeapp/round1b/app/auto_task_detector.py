import os
from PyPDF2 import PdfReader


def extract_text_from_pdfs(pdf_dir):
    all_text = ""
    for file in os.listdir(pdf_dir):
        if file.endswith(".pdf"):
            path = os.path.join(pdf_dir, file)
            try:
                reader = PdfReader(os.path.join(pdf_dir, file))
                for page in reader.pages:
                    if page.extract_text():
                        all_text += page.extract_text().lower() + "\n"
            except Exception as e:
                print(f"[!] Error reading {file}: {e}")
    return all_text


def best_match_category(text, category_dict, default_category):
    max_score = 0
    best_categories = []
    for cat, keywords in category_dict.items():
        score = sum(text.count(k.lower()) for k in keywords)
        if score > max_score:
            max_score = score
            best_categories = [cat]
        elif score == max_score and score > 0:
            best_categories.append(cat)

    if not best_categories:
        return default_category
    elif len(best_categories) == 1:
        return best_categories[0]
    else:
        return best_categories[0]  # deterministic fallback


def guess_persona(text):
    persona_keywords = {
        # Food & Cooking
        "Event Planner": ["cook", "home cooking", "recipe", "kitchen", "baking" , "ingredients" ,"recipe"],
        "Professional Chef": ["gourmet", "fine dining", "culinary school", "chef"],
        "Food Blogger": ["blog", "review", "instagram", "recipe blog"],
        "Nutritionist": ["nutrition", "calories", "diet", "macronutrient", "intake"],
        "Vegan Cook": ["plant-based", "vegan", "dairy-free", "meatless"],
        "Street Food Vendor": ["street food", "stall", "vendor", "hawker"],
        "Meal Planner Mom/Dad": ["meal prep", "family dinner", "kids lunch"],
        "Fitness Enthusiast (Meal Prepper)": ["protein", "meal prep", "macro"],
        "Restaurant Owner": ["menu design", "restaurant", "chef special"],
        "Budget Cook": ["affordable", "budget", "cheap meals"],

        # Education
        "School Teacher": ["lesson plan", "classroom", "syllabus", "students"],
        "College Professor": ["lecture", "university", "research", "term paper"],
        "Private Tutor": ["one-on-one", "tutor", "coaching"],
        "Principal / Administrator": ["school policy", "administration", "principal"],
        "Online Course Creator": ["course module", "e-learning", "platform", "LMS"],
        "EdTech Startup Founder": ["startup", "edtech", "platform", "scaling"],
        "Student (School/College)": ["exam", "semester", "notes", "textbook"],
        "Exam Aspirant (UPSC/NEET/JEE)": ["upsc", "neet", "jee", "prelims", "mock test"],
        "Research Scholar": ["hypothesis", "methodology", "journal", "peer-reviewed"],
        "Parent of Student": ["parent-teacher", "PTM", "child's progress"],

        # Healthcare
        "General Physician": ["patient", "symptom", "diagnosis"],
        "Surgeon": ["surgery", "operation", "post-op"],
        "Nurse": ["care", "vital signs", "shift", "ward"],
        "Pediatrician": ["child", "infant", "growth", "vaccination"],
        "Psychologist": ["therapy", "mental health", "anxiety", "depression"],
        "Physiotherapist": ["rehab", "muscle", "movement"],
        "Pharmacist": ["prescription", "drug", "pharmacy"],
        "Medical Lab Technician": ["lab test", "report", "specimen"],
        "Hospital Admin": ["facility", "hospital policy", "staffing"],
        "Medical Student": ["clinical rotation", "anatomy", "internship"],

        # Legal
        "Lawyer (Civil/Criminal)": ["case law", "plaintiff", "defendant"],
        "Judge": ["verdict", "courtroom", "hearing"],
        "Law Student": ["case brief", "judgment", "article"],
        "Legal Advisor": ["contract", "legal advice", "counsel"],
        "Legal Intern": ["internship", "chambers", "research"],
        "Corporate Lawyer": ["M&A", "corporate law", "shareholding"],
        "Family Lawyer": ["divorce", "custody", "alimony"],
        "Public Prosecutor": ["evidence", "trial", "prosecution"],
        "Legal Blogger": ["legal update", "judicial analysis"],
        "Legal Consultant": ["compliance", "risk"],

        "HR Professional": ["onboarding", "compliance", "fillable form", "acrobat", "employee record", "recruitment", "policy", "workforce", "attendance"],
        "Office Manager": ["task list", "approval", "workflow", "meeting", "share file", "pdf editor", "team lead", "project document"],
        "Corporate Document Reviewer": ["pdf comment", "annotation", "shared file", "text markup", "review link", "commenting tools", "editor"],
        "Admin Executive": ["document tracking", "request form", "submit report", "signature", "shared workspace", "edit access"],

        # Business & Finance
        "Investment Analyst": ["revenue", "fiscal year", "growth rate", "r&d", "shareholder", "quarterly report", "financial performance", "profit margin", "ebitda", "investment", "market strategy", "competitor analysis", "annual report", "stock performance", "valuation"],

        # Technology
        "Software Developer": ["code", "github", "repository", "function"],
        "Data Scientist": ["machine learning", "pandas", "dataset"],
        "UI/UX Designer": ["wireframe", "user experience", "figma"],
        "AI/ML Engineer": ["neural network", "deep learning", "transformer"],
        "Cybersecurity Analyst": ["vulnerability", "breach", "encryption"],
        "IT Project Manager": ["timeline", "scrum", "sprint"],
        "Tech Blogger": ["review", "tech trends", "gadgets"],
        "QA Tester": ["bug", "test case", "QA"],
        "Cloud Engineer": ["AWS", "GCP", "container", "Kubernetes"],
        "Tech Support Agent": ["ticket", "troubleshoot", "issue"],

        # Travel
        "Solo Traveller": ["solo trip", "hostel", "self-explore"],
        "Budget Backpacker": ["cheap stay", "budget", "hostel"],
        "Luxury Traveller": ["resort", "villa", "spa"],
        "Travel Agent": ["itinerary", "client trip"],
        "Adventure Seeker": ["hike", "trek", "bungee"],
        "Family Vacationer": ["family trip", "kids", "hotel stay"],

        # Influencers
        "Travel Vlogger": ["destination", "vlog", "journey", "trip"],
        "Fitness Influencer": ["gym", "workout", "nutrition"],
        "Meme Creator": ["meme", "funny", "viral"],
        "Digital Nomad": ["remote work", "lifestyle", "wifi", "laptop"],
        "Online Coach": ["course", "coaching", "clients"]
    }
    return best_match_category(text, persona_keywords, "Curious Reader")


def guess_job(text):
    job_keywords = {
        "Summarize the document's key findings": ["summarize", "overview", "abstract", "conclusion"],
        "Identify important concepts and topics for study": ["study", "prepare", "exam", "syllabus", "revision", "concept", "highlight"],
        "Compare and evaluate key metrics across documents": ["compare", "benchmark", "performance", "vs", "versus", "competitor"],
        "Write a literature review highlighting methodology and outcomes": ["literature review", "methods", "results", "experiment", "findings"],
        "Analyze trends and extract actionable insights": ["analyze", "report", "trend", "financials", "insight", "forecast"],
        "Analyze revenue trends, R&D investments, and market positioning strategies": ["annual report", "financial highlights", "revenue trends", "r&d spend", "market positioning", "shareholder letter", "earnings", "company performance", "investment highlights", "fiscal year", "business outlook"],
        "Create a syllabus and teaching strategy": ["lesson plan", "syllabus", "topic", "teaching strategy", "curriculum plan"],
        "Evaluate marketing effectiveness across channels": ["campaign", "market strategy", "roi", "branding", "engagement rate"],
        "Summarize clinical information for diagnosis or treatment": ["treatment plan", "diagnosis", "medical", "clinical findings", "protocol"],
        "Extract key insights to support a successful sales pitch": ["leads", "sales pitch", "objection handling", "crm insights", "client pain points"],
        "Plan a trip itinerary based on interest areas": ["plan", "days", "trip", "group", "places to visit", "itinerary", "schedule", "tourist spots", "booking"],
        "Plan a trip or itinerary for group travel": ["plan trip", "create itinerary", "travel route", "tour plan", "group travel", "trip plan", "explore", "organize vacation"],
        "Design a professional menu lineup featuring crowd-pleasing main courses": ["menu", "dish", "flavors", "course", "ingredients"],
        "Prepare a meal prep or weekly cooking plan": ["meal prep", "grocery list", "weekly menu", "planning meals"],
        "Draft a school policy or education proposal": ["school policy", "regulations", "administrative"],
        "Review a legal case and outline verdict implications": ["verdict", "judgment", "legal implications"],
        "Create and manage fillable forms for onboarding and compliance": ["acrobat", "pdf form", "fillable", "compliance", "onboarding", "form field", "submit", "signature", "employee form"],
        "Review, comment, and share documents collaboratively": ["comment", "review", "share link", "pdf comments", "highlight", "markup", "collaboration", "annotate"],
        "Manage and track internal document workflows across teams": ["workflow", "approve", "team document", "share", "task tracking", "request", "reviewer"],
        "Edit and distribute official communication documents": ["memo", "distribute", "shared note", "announcement", "notice", "approval"],
        "Build a data-driven dashboard or visualization": ["dashboard", "kpi", "data visualization"]
    }
    return best_match_category(text, job_keywords, "Extract the most relevant sections based on user goal")


def detect_task(input_dir="app/input"):
    raw_text = extract_text_from_pdfs(input_dir)
    print("[DEBUG] First 1000 characters of text:")
    print(raw_text[:1000])
    persona = guess_persona(raw_text)
    job = guess_job(raw_text)
    return persona, job


if __name__ == "__main__":
    p, j = detect_task()
    print("✅ Persona:", p)
    print("✅ Job to be done:", j)

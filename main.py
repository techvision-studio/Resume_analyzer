from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
import pdfplumber
import docx

# If resume_parser has issues, consider using NLP-based extractions instead
try:
    from resume_parser import extract_skills, extract_education, extract_contact_details, match_resume_with_job
except ImportError:
    def extract_skills(text): return ["Skill extraction not available"]
    def extract_education(text): return ["Education extraction not available"]
    def extract_contact_details(text): return {"phone": "N/A", "email": "N/A"}
    def match_resume_with_job(text, job_description): return "N/A"

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_text_from_pdf(file):
    """Extract text from a PDF file."""
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
    return text.strip() if text else "No text found"

def extract_text_from_docx(file):
    """Extract text from a DOCX file."""
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip() if text else "No text found"

@app.post("/analyze-resume/")
async def analyze_resume(file: UploadFile = File(...)):
    file_ext = file.filename.split(".")[-1].lower()
    content = await file.read()
    
    if file_ext == "pdf":
        text = extract_text_from_pdf(BytesIO(content))
    elif file_ext == "docx":
        text = extract_text_from_docx(BytesIO(content))
    else:
        return {"error": "Unsupported file format"}

    skills = extract_skills(text)
    education = extract_education(text)
    contact_info = extract_contact_details(text)

    return {
        "filename": file.filename,
        "skills": skills,
        "education": education,
        "contact_info": contact_info,
        "extracted_text": text[:500],  # Limit output for debugging
    }

@app.post("/match-resume/")
async def match_resume(file: UploadFile = File(...), job_description: str = ""):
    file_ext = file.filename.split(".")[-1].lower()
    content = await file.read()

    if file_ext == "pdf":
        text = extract_text_from_pdf(BytesIO(content))
    elif file_ext == "docx":
        text = extract_text_from_docx(BytesIO(content))
    else:
        return {"error": "Unsupported file format"}

    match_score = match_resume_with_job(text, job_description)

    return {
        "filename": file.filename,
        "match_score": f"{match_score}%",  # Return Match Percentage
    }

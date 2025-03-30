import spacy
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Predefined skills list (can be expanded)
SKILLS = [
    "Python", "Java", "SQL", "Machine Learning", "Deep Learning", "Data Science", "C++", "JavaScript"
]

SOFT_SKILLS = [
    "Leadership", "Communication", "Teamwork", "Problem-solving", "Time management", "Creativity"
]


def extract_skills(text):
    doc = nlp(text)
    extracted_skills = {token.text for token in doc if token.text in SKILLS}
    return list(extracted_skills)


def extract_education(text):
    education_pattern = r"(Bachelor|Master|B\.Sc|M\.Sc|PhD|BTech|MTech|MBA|Diploma|BE|B\.E)[^\n,]+"
    education = re.findall(education_pattern, text, re.IGNORECASE)
    return education if education else ["Not found"]


def extract_contact_details(text):
    phone_pattern = r"\+?\d{1,4}[-.\s]?\(?\d{2,5}\)?[-.\s]?\d{3,5}[-.\s]?\d{3,5}"
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    linkedin_pattern = r"https?://(www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+"
    phone = re.findall(phone_pattern, text)
    email = re.findall(email_pattern, text)
    linkedin = re.findall(linkedin_pattern, text)
    return {"phone": phone[0] if phone else "Not found", "email": email[0] if email else "Not found", "linkedin": linkedin[0] if linkedin else "Not found"}


def extract_experience(text):
    experience_pattern = r"(\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s\d{4}\b)[^\n]+"
    matches = re.findall(experience_pattern, text, re.IGNORECASE)
    return matches if matches else ["Not found"]


def extract_projects(text):
    project_pattern = r"(?:Project:|Developed|Built|Worked on)[^\n]+"
    projects = re.findall(project_pattern, text, re.IGNORECASE)
    return projects if projects else ["Not found"]


def extract_certifications(text):
    cert_pattern = r"(?:Certified|Certification|Course|Training)[:\s\w,&.-]+"
    certifications = re.findall(cert_pattern, text, re.IGNORECASE)
    return certifications if certifications else ["Not found"]


def extract_soft_skills(text):
    extracted_skills = {skill for skill in SOFT_SKILLS if skill.lower() in text.lower()}
    return list(extracted_skills) if extracted_skills else ["Not found"]


def match_resume_with_job(resume_text, job_description):
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text, job_description])
    similarity = cosine_similarity(vectors)[0, 1]
    return round(similarity * 100, 2)
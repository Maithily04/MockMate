"""
====================================================
MockMate AI - Resume Parser
----------------------------------------------------
Reads PDF, DOCX and TXT resumes and extracts
resume text and technical skills.

Author : Maithily Bhatt
====================================================
"""

import os
import pdfplumber
from docx import Document

SKILLS = {
    "python", "java", "c", "c++", "html", "css", "javascript", "react", "nodejs",
    "flask", "django", "sql", "mysql", "sqlite", "mongodb", "dbms", "operating system",
    "os", "computer networks", "cn", "oops", "oop", "data structures", "dsa",
    "machine learning", "deep learning", "artificial intelligence", "ai", "nlp",
    "opencv", "tensorflow", "keras", "pytorch", "numpy", "pandas", "matplotlib",
    "seaborn", "git", "github", "linux", "aws", "firebase"
}

def read_pdf(filepath):
    text = ""
    try:
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def read_docx(filepath):
    text = ""
    try:
        document = Document(filepath)
        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX: {e}")
    return text

def read_txt(filepath):
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
            return file.read()
    except Exception as e:
        print(f"Error reading TXT: {e}")
        return ""

def extract_resume_text(filepath):
    extension = os.path.splitext(filepath)[1].lower()
    if extension == ".pdf":
        return read_pdf(filepath)
    elif extension == ".docx":
        return read_docx(filepath)
    elif extension == ".txt":
        return read_txt(filepath)
    return ""

def extract_skills(text):
    text = text.lower()
    detected_skills = []
    for skill in sorted(SKILLS):
        if skill in text:
            detected_skills.append(skill.title())
    return detected_skills

def parse_resume(filepath):
    resume_text = extract_resume_text(filepath)
    skills = extract_skills(resume_text)
    return {
        "text": resume_text,
        "skills": skills
    }
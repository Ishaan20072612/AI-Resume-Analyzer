"""
Resume Analyzer — Core logic using Groq (free)
"""

import os
import json
from groq import Groq

SYSTEM_PROMPT = """You are an expert technical recruiter and career coach with 15 years of experience 
hiring for top tech companies. You analyze resumes against job descriptions with precision and honesty.

You always respond in this exact JSON format (no markdown, no preamble, no backticks):
{
  "match_score": <integer 0-100>,
  "verdict": "<one line overall assessment>",
  "strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
  "missing_skills": ["<skill 1>", "<skill 2>", "<skill 3>"],
  "improvements": ["<improvement 1>", "<improvement 2>", "<improvement 3>"],
  "ats_tips": ["<tip 1>", "<tip 2>"],
  "hire_recommendation": "<Strong Yes / Yes / Maybe / No>"
}"""


def analyze_resume(resume_text: str, job_description: str, api_key: str) -> dict:
    """Analyze resume against job description using Groq."""
    client = Groq(api_key=api_key)
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"""Analyze this resume against the job description below.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Respond ONLY with the JSON object, nothing else."""}
        ],
        temperature=0.3,
        max_tokens=1500,
    )
    
    text = response.choices[0].message.content.strip()
    text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract text from PDF using pdfplumber."""
    import pdfplumber
    import io
    text = ""
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.strip()

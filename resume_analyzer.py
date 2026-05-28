"""
Resume Analyzer — Core logic using Anthropic API
"""

import os
import base64
from anthropic import Anthropic

client = Anthropic()

SYSTEM_PROMPT = """You are an expert technical recruiter and career coach with 15 years of experience 
hiring for top tech companies. You analyze resumes against job descriptions with precision and honesty.

When analyzing, you always respond in this exact JSON format (no markdown, no preamble):
{
  "match_score": <integer 0-100>,
  "verdict": "<one line overall assessment>",
  "strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
  "missing_skills": ["<skill 1>", "<skill 2>", "<skill 3>"],
  "improvements": ["<improvement 1>", "<improvement 2>", "<improvement 3>"],
  "ats_tips": ["<tip 1>", "<tip 2>"],
  "hire_recommendation": "<Strong Yes / Yes / Maybe / No>"
}"""


def analyze_resume(resume_text: str, job_description: str) -> dict:
    """Analyze resume against job description using Claude."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"""Analyze this resume against the job description below.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Provide your analysis in the exact JSON format specified."""
        }]
    )
    
    import json
    text = response.content[0].text.strip()
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

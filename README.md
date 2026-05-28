# AI Resume Analyzer

An AI-powered resume analyzer that scores your resume against a job description, identifies skill gaps, and gives ATS optimization tips — built with Llama 3.3 70B via Groq and Streamlit. Completely free to use.

---

## What It Does

Upload your resume PDF and paste a job description. The AI analyzes:

- **Match score** — how well your resume fits the role (0–100)
- **Strengths** — what you're doing right
- **Missing skills** — gaps between your profile and the job requirements
- **Improvements** — specific suggestions to strengthen your resume
- **ATS tips** — how to optimize for applicant tracking systems
- **Hire recommendation** — Strong Yes / Yes / Maybe / No

---

## Live Demo

[Open the app](https://ai-resume-analyzer-ic.streamlit.app)

> Get a free Groq API key at [console.groq.com](https://console.groq.com) — no credit card required.

---

## Local Setup

```bash
git clone https://github.com/Ishaan20072612/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
pip install -r requirements.txt
streamlit run resume_app.py
```

Enter your free Groq API key in the sidebar when the app opens.

---

## Project Structure

```
├── resume_app.py       # Streamlit UI
├── resume_analyzer.py  # Groq + Llama 3.3 analysis logic
├── requirements.txt    # Dependencies
└── README.md
```

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| `groq` | Llama 3.3 70B inference (free) |
| `pdfplumber` | PDF text extraction |
| `streamlit` | Web UI |

---

## Why Groq

Groq provides free API access to Llama 3.3 70B — one of the most capable open-source models available. No credit card required, generous free tier, and extremely fast inference.

---

## Author

Ishaan Chowdhury · [@Ishaan20072612](https://github.com/Ishaan20072612)

"""
Resume Analyzer — Streamlit UI (Groq powered)
"""

import streamlit as st
from resume_analyzer import analyze_resume, extract_text_from_pdf

st.set_page_config(page_title="Resume Analyzer", page_icon="📄", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');
    html, body, [class*="css"] { font-family: 'Syne', sans-serif; background-color: #0a0a0a; color: #f0f0f0; }
    .main { background-color: #0a0a0a; }
    .hero-title { font-size: 3rem; font-weight: 800; letter-spacing: -2px; background: linear-gradient(135deg, #f0f0f0 0%, #888 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1.1; margin-bottom: 8px; }
    .hero-sub { font-family: 'DM Mono', monospace; font-size: 0.85rem; color: #555; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 40px; }
    .score-ring { text-align: center; padding: 32px; background: #111; border: 1px solid #222; border-radius: 16px; margin-bottom: 20px; }
    .score-number { font-size: 5rem; font-weight: 800; letter-spacing: -4px; line-height: 1; }
    .score-label { font-family: 'DM Mono', monospace; font-size: 0.75rem; color: #555; text-transform: uppercase; letter-spacing: 2px; margin-top: 8px; }
    .verdict-box { background: #111; border: 1px solid #222; border-left: 3px solid #f0f0f0; border-radius: 8px; padding: 16px 20px; font-size: 0.95rem; line-height: 1.6; color: #ccc; margin-bottom: 20px; }
    .section-card { background: #111; border: 1px solid #1e1e1e; border-radius: 12px; padding: 20px 24px; margin-bottom: 16px; }
    .section-title { font-family: 'DM Mono', monospace; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 3px; color: #555; margin-bottom: 14px; }
    .tag { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; margin: 3px; font-family: 'DM Mono', monospace; }
    .tag-green { background: #0d2018; color: #4ade80; border: 1px solid #14532d; }
    .tag-red { background: #2d0d0d; color: #f87171; border: 1px solid #7f1d1d; }
    .hire-badge { display: inline-block; padding: 8px 20px; border-radius: 6px; font-weight: 700; font-size: 0.9rem; letter-spacing: 1px; font-family: 'DM Mono', monospace; }
    .hire-yes { background: #0d2018; color: #4ade80; border: 1px solid #14532d; }
    .hire-maybe { background: #1f1a07; color: #fbbf24; border: 1px solid #713f12; }
    .hire-no { background: #2d0d0d; color: #f87171; border: 1px solid #7f1d1d; }
    .stButton > button { background: #f0f0f0 !important; color: #0a0a0a !important; border: none !important; border-radius: 8px !important; font-family: 'Syne', sans-serif !important; font-weight: 700 !important; font-size: 0.9rem !important; letter-spacing: 1px !important; padding: 12px 32px !important; width: 100% !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero-title">Resume<br>Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">AI-powered · Instant feedback · ATS optimized · Free</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Groq API Key")
    st.markdown("**Free** — get yours at [console.groq.com](https://console.groq.com)")
    api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
    st.caption("Free to use. Key is only held in memory.")
    st.divider()
    st.markdown("### How it works")
    st.markdown("""
1. Get a free Groq API key at console.groq.com
2. Upload your resume PDF
3. Paste the job description
4. Get instant AI analysis:
   - Match score (0-100)
   - Strengths & skill gaps
   - ATS optimization tips
   - Hire recommendation
    """)
    st.divider()
    st.markdown("### Model")
    st.markdown("Llama 3.3 70B via Groq — fast and free")

col1, col2 = st.columns(2, gap="large")
with col1:
    st.markdown("#### Resume")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")
    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")

with col2:
    st.markdown("#### Job Description")
    job_description = st.text_area("Paste job description", height=200, placeholder="Paste the full job description here...", label_visibility="collapsed")

st.write("")
analyze_btn = st.button("ANALYZE RESUME", use_container_width=True)

if analyze_btn:
    if not api_key:
        st.error("Please enter your free Groq API key in the sidebar. Get one at console.groq.com")
        st.stop()
    if not uploaded_file:
        st.error("Please upload a resume PDF.")
        st.stop()
    if not job_description.strip():
        st.error("Please paste a job description.")
        st.stop()

    with st.spinner("Analyzing your resume..."):
        try:
            pdf_bytes = uploaded_file.read()
            resume_text = extract_text_from_pdf(pdf_bytes)
            if not resume_text:
                st.error("Could not extract text from PDF.")
                st.stop()
            result = analyze_resume(resume_text, job_description, api_key)
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
            st.stop()

    st.divider()
    st.markdown("## Analysis Results")
    st.write("")

    score_col, verdict_col = st.columns([1, 2], gap="large")
    with score_col:
        score = result.get("match_score", 0)
        color = "#4ade80" if score >= 75 else ("#fbbf24" if score >= 50 else "#f87171")
        st.markdown(f'<div class="score-ring"><div class="score-number" style="color:{color}">{score}</div><div class="score-label">Match Score / 100</div></div>', unsafe_allow_html=True)
        hire = result.get("hire_recommendation", "Maybe")
        hire_class = "hire-yes" if "Yes" in hire else ("hire-no" if hire == "No" else "hire-maybe")
        st.markdown(f'<div style="text-align:center"><div style="font-family:\'DM Mono\',monospace;font-size:0.7rem;color:#555;text-transform:uppercase;letter-spacing:2px;margin-bottom:8px">Hire Recommendation</div><span class="hire-badge {hire_class}">{hire}</span></div>', unsafe_allow_html=True)

    with verdict_col:
        st.markdown(f'<div class="verdict-box">{result.get("verdict", "")}</div>', unsafe_allow_html=True)
        strengths = result.get("strengths", [])
        if strengths:
            st.markdown('<div class="section-card"><div class="section-title">Strengths</div>' + "".join([f'<span class="tag tag-green">{s}</span>' for s in strengths]) + '</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        missing = result.get("missing_skills", [])
        if missing:
            st.markdown('<div class="section-card"><div class="section-title">Missing Skills</div>' + "".join([f'<span class="tag tag-red">{s}</span>' for s in missing]) + '</div>', unsafe_allow_html=True)
        ats = result.get("ats_tips", [])
        if ats:
            items = "".join([f"<li style='margin-bottom:8px;color:#aaa;font-size:0.85rem'>{t}</li>" for t in ats])
            st.markdown(f'<div class="section-card"><div class="section-title">ATS Tips</div><ul style="margin:0;padding-left:18px">{items}</ul></div>', unsafe_allow_html=True)

    with col_b:
        improvements = result.get("improvements", [])
        if improvements:
            items = "".join([f"<li style='margin-bottom:8px;color:#aaa;font-size:0.85rem'>{i}</li>" for i in improvements])
            st.markdown(f'<div class="section-card"><div class="section-title">Improvements</div><ul style="margin:0;padding-left:18px">{items}</ul></div>', unsafe_allow_html=True)

import streamlit as st
st.set_page_config(page_title="SkillAlign AI - Dashboard", layout="centered")
from utils.jd_skill_extractor import extract_skills_from_jd
from utils.matcher import match_resume_with_jd
from utils.resume_writer import generate_resume
import base64
import os


if not st.session_state.get("logged_in"):
    st.warning("Please log in first.")
    st.stop()

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.user_info = {}
    st.rerun()

user_info = st.session_state.get("user_info", {})

st.title("📄 SkillAlign AI Dashboard")

st.markdown(f"Welcome, **{st.session_state['user_info']['full_name']}** 👋")

# Upload resume and job info
st.header("📥 Upload Resume & Job Details")

uploaded_resume = st.file_uploader("Upload your existing resume (PDF only)", type=["pdf"])
job_title = st.text_input("Enter the Job Title you're targeting")
job_description = st.text_area("Paste the Job Description here")

if st.button("Analyze"):
    if uploaded_resume and job_description:
        resume_text = uploaded_resume.read().decode("latin-1", errors="ignore")
        jd_skills = extract_skills_from_jd(job_description)
        matched, missing, score = match_resume_with_jd(resume_text, jd_skills)

        st.success(f"✅ Similarity Score: {score:.2f}%")

        st.subheader("🧠 Skill Gap Report")
        st.markdown(f"**Matched Skills:** {', '.join(matched) if matched else 'None'}")
        st.markdown(f"**Missing Skills:** {', '.join(missing) if missing else 'None'}")

        st.subheader("📄 Generate Optimized Resume")

        # You can later replace below with user info from DB
        full_name = "Your Name"
        skills = ", ".join(matched + missing)
        optimized_resume_path = generate_resume(full_name, skills, job_title, matched, missing)

        with open(optimized_resume_path, "rb") as file:
            b64 = base64.b64encode(file.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="Optimized_Resume.pdf">📥 Download Optimized Resume</a>'
            st.markdown(href, unsafe_allow_html=True)

    else:
        st.warning("Please upload resume and job description.")

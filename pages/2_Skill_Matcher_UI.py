import streamlit as st
from utils.jd_skill_extractor import extract_skills_from_jd
from utils.resume_parser import extract_skills_from_resume
from utils.matcher import get_skill_gap_and_similarity
from utils.resume_writer import generate_resume
import base64

st.set_page_config(page_title="SkillAlignAI - Skill Matcher", layout="centered")

# 🔐 Ensure user is logged in
if not st.session_state.get("logged_in"):
    st.warning("Please log in first.")
    st.stop()

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.user_info = {}
    st.rerun()

user_info = st.session_state.get("user_info", {})

def skill_matcher_interface(user_info):
    st.subheader("🎯 Target Job Role Skill Matcher")

    st.markdown(f"Welcome back, **{user_info['full_name']}** 👋")

    # Resume upload + job input
    resume_file = st.file_uploader("📄 Upload your current resume (PDF)", type=['pdf'])
    job_title = st.text_input("💼 Target Job Title")
    job_description = st.text_area("📝 Paste Job Description")

    if st.button("Analyze & Generate Resume"):
        if not resume_file or not job_title or not job_description:
            st.warning("Please upload a resume and fill in job details.")
            return

        with st.spinner("🔍 Analyzing your profile and job description..."):

            # Extract skills from resume + JD
            user_resume_skills = extract_skills_from_resume(resume_file)
            jd_skills = extract_skills_from_jd(job_description)

            missing_skills, similarity_score = get_skill_gap_and_similarity(user_resume_skills, jd_skills)

            # Get projects, certifications, summary from profile
            projects = user_info.get("projects", "")
            certifications = user_info.get("certifications", "")
            summary = user_info.get("summary", "")

            # Let user review profile info before generating
            st.subheader("📝 Profile Info to Use in Resume")

            editable_summary = st.text_area("Professional Summary", summary, max_chars=500)
            editable_skills = st.text_area("Skills", ", ".join(user_resume_skills), help="Separate skills with commas")
            editable_projects = st.text_area("Projects", projects, help="Separate multiple projects with commas")
            editable_certs = st.text_area("Certifications", certifications, help="Separate multiple certifications with commas")

            # Generate tailored resume
            tailored_resume_path = generate_resume(
                user_info["full_name"],
                editable_skills,
                job_title,
                user_resume_skills,
                missing_skills,
                editable_projects,
                editable_certs,
                editable_summary
            )

        # Show results
        st.success("✅ Analysis Complete!")
        st.metric("Similarity Score", f"{similarity_score:.2f}%")
        st.markdown("**🔧 Missing Skills:**")
        st.write(", ".join(missing_skills) if missing_skills else "No major gaps found!")

        # Download option
        with open(tailored_resume_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="Tailored_Resume.pdf">📥 Download Optimized Resume</a>'
            st.markdown(href, unsafe_allow_html=True)

# Run interface
skill_matcher_interface(user_info)

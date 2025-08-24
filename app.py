import streamlit as st
import os
from utils.jd_skill_extractor import extract_skills_from_jd
from utils.matcher import match_resume_with_jd
from utils.resume_writer import generate_resume
from auth_ui import auth_interface

# Set Streamlit config
st.set_page_config(page_title="SkillAlignAI", layout="centered")

def main():
    st.title("📄 SkillAlignAI - ATS-Friendly Resume Generator")

    # Auth system
    if not st.session_state.get("logged_in"):
        auth_interface()
        return

    # Load user info
    user_info = st.session_state.user_info
    user_name = user_info.get("full_name", "")
    user_skills = user_info.get("skills", "")

    # Sidebar info display
    st.sidebar.title("👤 User Info")
    st.sidebar.markdown(f"**Name:** {user_name}")
    st.sidebar.markdown(f"**Skills:** {user_skills}")

    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_info = {}
        st.rerun()
    
    # Resume upload
    st.header("📤 Upload Your Resume")
    resume_file = st.file_uploader("Upload your current resume (TXT format)", type=["txt"])

    # JD input
    st.header("🧾 Job Description Input")
    job_title = st.text_input("Target Job Title")
    job_description = st.text_area("Paste the job description here", height=200)

    # On button click
    if st.button("🔍 Analyze & Generate Resume"):
        if resume_file is None or not job_title or not job_description:
            st.warning("Please upload resume and enter job title + description.")
        else:
            resume_text = resume_file.read().decode("utf-8")
            jd_skills = extract_skills_from_jd(job_description)
            matched_skills, missing_skills, similarity_score = match_resume_with_jd(resume_text, jd_skills)

            # Display result
            st.success("✅ Skill Gap Analysis Completed!")
            st.metric("Similarity Score", f"{similarity_score:.2f}%")
            st.markdown(f"**Matched Skills:** {', '.join(matched_skills) if matched_skills else 'None'}")
            st.markdown(f"**Missing Skills:** {', '.join(missing_skills) if missing_skills else 'None'}")

            # Generate tailored resume
            output_path = generate_resume(user_name, user_skills, job_title, matched_skills, missing_skills)

            with open(output_path, "rb") as f:
                st.download_button("📥 Download Optimized Resume", f, file_name="Optimized_Resume.pdf")

    # Footer
    st.markdown("---")
    st.caption("🚀 Built with Streamlit | SkillAlignAI 2025")

if __name__ == "__main__":
    main()

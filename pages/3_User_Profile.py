import streamlit as st
from db.user_queries import get_user_by_username, update_user_info

st.set_page_config(page_title="SkillAlignAI - Profile", layout="centered")
st.title("👤 Your Profile")

# 🔐 Check login
if not st.session_state.get("logged_in"):
    st.warning("Please log in to view your profile.")
    st.stop()

# 📤 Load from session
user = st.session_state.get("user_info")
username = user['username']

# 🔄 Load from database
user_data = get_user_by_username(username)
if not user_data:
    st.error("User not found.")
    st.stop()

# ----------------------------
# 🎯 Editable Profile Form
# ----------------------------
st.markdown("### 🧾 Update Profile Information")

# Full Name
full_name = st.text_input("👤 Full Name", value=user_data.get("full_name") or "")

# Email
email = st.text_input("📧 Email", value=user_data.get("email") or "")

# Education
education_levels = ["High School", "Diploma", "Bachelor's Degree", "Master's Degree", "PhD", "Other"]
selected_level = st.selectbox("🎓 Highest Education", education_levels, index=education_levels.index("Bachelor's Degree") if user_data.get("education") else 0)
education_details = st.text_input("📘 Education Details (e.g., B.Tech in AIML, GH Raisoni College)", value=user_data.get("education") or "")

# Skills (Multi-Select)
available_skills = ["Python", "SQL", "Machine Learning", "Deep Learning", "NLP", "Flask", "Streamlit", "Tableau", "Power BI", "Data Analysis", "Java", "C++", "AWS", "Docker"]
skills_selected = st.multiselect("🛠 Skills (select multiple)", available_skills, default=(user_data.get("skills") or "").split(", "))

# Projects
projects = st.text_area("📂 Projects (separate by commas)", value=user_data.get("projects") or "")

# Certifications
certifications = st.text_area("📜 Certifications (separate by commas)", value=user_data.get("certifications") or "")

# Summary (300 characters max)
summary = st.text_area("📝 Professional Summary (max 300 characters)", value=user_data.get("summary") or "", max_chars=300)
st.caption(f"Characters used: {len(summary)}/300")

# ----------------------------
# 💾 Save Updates
# ----------------------------
if st.button("💾 Save Profile"):
    update_user_info(username, "full_name", full_name)
    update_user_info(username, "email", email)
    update_user_info(username, "education", education_details)
    update_user_info(username, "skills", ", ".join(skills_selected))
    update_user_info(username, "projects", projects)
    update_user_info(username, "certifications", certifications)
    update_user_info(username, "summary", summary)

    # Update session state too
    st.session_state.user_info.update({
        "full_name": full_name,
        "email": email,
        "education": education_details,
        "skills": ", ".join(skills_selected),
        "projects": projects,
        "certifications": certifications,
        "summary": summary
    })

    st.success("✅ Profile updated successfully!")

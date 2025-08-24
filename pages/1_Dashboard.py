import streamlit as st
from utils.jd_skill_extractor import extract_skills_from_jd
from utils.matcher import match_resume_with_jd

st.set_page_config(page_title="SkillAlignAI - Dashboard", layout="centered")

# 🔐 Login Check
if not st.session_state.get("logged_in"):
    st.warning("Please log in first.")
    st.stop()

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.user_info = {}
    st.rerun()

user_info = st.session_state.get("user_info", {})

st.title("📊 SkillAlignAI Dashboard")
st.markdown(f"Welcome, **{user_info['full_name']}** 👋")

# ----------------------------
# 🔍 Profile Completeness Check
# ----------------------------
required_fields = ["full_name", "education", "skills", "projects", "certifications", "summary"]
missing_fields = [field for field in required_fields if not user_info.get(field)]

if missing_fields:
    st.error("⚠️ Your profile is incomplete. Please update the following fields before using the system:")
    st.write(", ".join([f.replace("_", " ").title() for f in missing_fields]))
    st.markdown("👉 Go to **👤 Profile** page and complete your details.")
    st.stop()

st.success("✅ Profile is complete! You can now use the system.")

# ----------------------------
# 📌 Quick Profile Overview
# ----------------------------
st.subheader("👤 Profile Snapshot")
st.markdown(f"**Education:** {user_info.get('education')}")
st.markdown(f"**Skills:** {user_info.get('skills')}")
st.markdown(f"**Projects:** {user_info.get('projects')}")
st.markdown(f"**Certifications:** {user_info.get('certifications')}")
st.markdown(f"**Summary:** {user_info.get('summary')}")

# ----------------------------
# 🚀 Next Step Navigation
# ----------------------------
st.markdown("---")
st.subheader("🚀 Ready to Optimize Your Resume?")

col1, col2 = st.columns(2)

with col1:
    if st.button("🧠 Go to Skill Matcher"):
        st.switch_page("pages/2_Skill_Matcher_UI.py")

with col2:
    if st.button("👤 Edit Profile"):
        st.switch_page("pages/3_User_Profile.py")

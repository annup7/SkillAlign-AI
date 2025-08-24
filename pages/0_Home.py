import streamlit as st

st.set_page_config(page_title="SkillAlignAI - Home", layout="centered")

# Title & Branding
st.title("💼 SkillAlignAI")
st.subheader("Your AI-Powered Resume Optimizer and Skill Matcher")

st.markdown("""
Welcome to **SkillAlignAI**, an intelligent platform designed to help job seekers tailor their resumes to job descriptions, analyze skill gaps, and boost their chances of landing interviews.

---

### 🔍 Features
- ✅ **Skill Gap Analysis**: Compare your resume against job descriptions.
- ✅ **Resume Optimization**: Generate ATS-friendly, tailored resumes using AI.
- ✅ **Login & Save Profiles**: Store your resume and skills securely.
- ✅ **Real-time Suggestions**: Get feedback based on the job market.
""")

# 🔐 Login Verification
if not st.session_state.get("logged_in"):
    st.warning("🔐 Please log in from the main menu (Login/Signup) to access platform features.")
    st.stop()

# 🟢 Logged in message
st.success(f"Welcome back, {st.session_state.user_info.get('full_name')} 👋")

# 🧭 Navigation Buttons
st.markdown("### 🔧 What would you like to do?")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Dashboard"):
        st.switch_page("1_Dashboard")

with col2:
    if st.button("🧠 Skill Matcher"):
        st.switch_page("2_Skill_Matcher_UI")

with col3:
    if st.button("👤 Profile"):
        st.switch_page("3_User_Profile")

# 🚪 Logout Button in Sidebar
st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.user_info = {}
    st.experimental_rerun()

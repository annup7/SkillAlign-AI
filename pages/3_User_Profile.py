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

# 🎯 Editable fields
st.markdown("### 🧾 Profile Details")
editable_fields = ["full_name", "email", "education", "skills", "projects", "certifications", "summary"]
updated_data = {}

for field in editable_fields:
    updated_data[field] = st.text_area(
        label=field.replace("_", " ").title(),
        value=user_data[field] or "",
        height=100
    )

# 💾 Save updates
if st.button("💾 Save Changes"):
    for field, value in updated_data.items():
        update_user_info(username, field, value)
    st.success("✅ Profile updated successfully! Refresh to view updated data.")

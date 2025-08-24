import streamlit as st
from auth_ui import auth_interface

# Must be called once at very start
st.set_page_config(page_title="SkillAlignAI", layout="centered")

def main():
    # If user not logged in → show login/signup
    if not st.session_state.get("logged_in"):
        auth_interface()
    else:
        st.switch_page("pages/0_Home.py")

if __name__ == "__main__":
    main()

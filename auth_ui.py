import streamlit as st
from auth import register_user, login_user

def signup_form():
    st.subheader("Create an Account")
    with st.form("signup_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        full_name = st.text_input("Full Name")
        password = st.text_input("Password", type="password")
        education = st.text_area("Education")
        skills = st.text_area("Skills (comma separated)")
        projects = st.text_area("Projects")
        certifications = st.text_area("Certifications")
        summary = st.text_area("Professional Summary")
        submitted = st.form_submit_button("Sign Up")

        if submitted:
            if username and email and password:
                try:
                    register_user(username, email, password, full_name, education, skills, projects, certifications, summary)
                    st.success("Account created successfully! Please login.")
                    st.session_state.page = "login"
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please fill all required fields.")

def login_form():
    st.subheader("Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            user = login_user(username, password)
            if user:
                st.success("Login successful!")
                st.session_state.logged_in = True
                st.session_state.user_info = dict(user._mapping)
            else:
                st.error("Invalid credentials.")

def auth_interface():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "page" not in st.session_state:
        st.session_state.page = "login"

    if st.session_state.page == "signup":
        signup_form()
        st.markdown("Already have an account? [Login](#)", unsafe_allow_html=True)
        if st.button("Go to Login"):
            st.session_state.page = "login"

    elif st.session_state.page == "login":
        login_form()
        st.markdown("Don't have an account? [Sign Up](#)", unsafe_allow_html=True)
        if st.button("Create New Account"):
            st.session_state.page = "signup"

import streamlit as st
from auth import register_user, login_user

# -------------------------
# Signup Form
# -------------------------
def signup_form():
    st.subheader("🆕 Create New Account")

    username = st.text_input("Username", key="signup_username")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")

    if st.button("Sign Up", key="signup_btn"):
        if username and email and password:
            try:
                register_user(username, email, password, None, None, None, None, None)
                st.success("✅ Account created successfully! Please log in.")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please fill all fields.")

# -------------------------
# Login Form (with Email)
# -------------------------
def login_form():
    st.subheader("🔐 Login to Your Account")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_btn"):
        if email and password:
            user = login_user(email, password)   # login using email
            if user:
                st.session_state.logged_in = True
                st.session_state.user_info = dict(user)
                st.success("✅ Logged in successfully!")
                st.experimental_rerun()
            else:
                st.error("Invalid email or password.")
        else:
            st.warning("Please enter both fields.")

# -------------------------
# Main Interface
# -------------------------
def auth_interface():
    choice = st.radio("Choose an option", ["Login", "Sign Up"], key="auth_choice")

    if choice == "Login":
        login_form()
    else:
        signup_form()

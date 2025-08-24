import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
import hashlib
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env")

# DB connection
DB_URL = os.getenv("NEON_DB_URL")
engine = create_engine(DB_URL, connect_args={"sslmode": "require"})

# Optional: debug DB URL (remove in production)
# print("DB URL:", DB_URL)

# 🔐 Password hasher
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 📝 Register a new user
def register_user(username, email, password, full_name, education, skills, projects, certifications, summary):
    hashed_pwd = hash_password(password)
    try:
        with engine.begin() as conn:
            conn.execute(
                text("""
                    INSERT INTO users (username, email, password, full_name, education, skills, projects, certifications, summary)
                    VALUES (:username, :email, :password, :full_name, :education, :skills, :projects, :certifications, :summary)
                """),
                {
                    "username": username,
                    "email": email,
                    "password": hashed_pwd,
                    "full_name": full_name,
                    "education": education,
                    "skills": skills,
                    "projects": projects,
                    "certifications": certifications,
                    "summary": summary
                }
            )
    except IntegrityError as e:
        error_message = str(e.orig).lower()
        if "username" in error_message:
            raise Exception("❌ Username already exists.")
        elif "email" in error_message:
            raise Exception("❌ Email already registered.")
        else:
            raise Exception("❌ Registration failed. Please try again.")

# 🔐 Validate login credentials
def login_user(username, password):
    hashed_pwd = hash_password(password)
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM users WHERE username = :username AND password = :password"),
            {"username": username, "password": hashed_pwd}
        ).fetchone()
    return result

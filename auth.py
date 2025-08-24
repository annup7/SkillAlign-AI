import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

# -------------------------
# Database Connection
# -------------------------
DB_URL = os.getenv("NEON_DB_URL")
engine = create_engine(DB_URL, echo=False, future=True)

# -------------------------
# Register New User
# -------------------------
def register_user(username, email, password, full_name=None, education=None, skills=None, projects=None, certifications=None, summary=None):
    with engine.begin() as conn:
        query = text("""
            INSERT INTO users (username, email, password, full_name, education, skills, projects, certifications, summary)
            VALUES (:username, :email, crypt(:password, gen_salt('bf')), :full_name, :education, :skills, :projects, :certifications, :summary)
        """)
        conn.execute(query, {
            "username": username,
            "email": email,
            "password": password,
            "full_name": full_name,
            "education": education,
            "skills": skills,
            "projects": projects,
            "certifications": certifications,
            "summary": summary
        })

# -------------------------
# Login with Email + Password
# -------------------------
def login_user(email, password):
    with engine.connect() as conn:
        query = text("""
            SELECT * FROM users
            WHERE email = :email AND password = crypt(:password, password)
        """)
        result = conn.execute(query, {"email": email, "password": password}).mappings().first()
        return result

# -------------------------
# Get User by Username
# -------------------------
def get_user_by_username(username):
    with engine.connect() as conn:
        query = text("SELECT * FROM users WHERE username = :username")
        result = conn.execute(query, {"username": username}).mappings().first()
        return result

# -------------------------
# Get User by Email
# -------------------------
def get_user_by_email(email):
    with engine.connect() as conn:
        query = text("SELECT * FROM users WHERE email = :email")
        result = conn.execute(query, {"email": email}).mappings().first()
        return result

# -------------------------
# Update User Information
# -------------------------
def update_user_info(identifier, field, value, by="email"):
    """
    Update user info by email (default) or username.
    """
    with engine.begin() as conn:
        if by == "email":
            query = text(f"UPDATE users SET {field} = :value WHERE email = :identifier")
        else:
            query = text(f"UPDATE users SET {field} = :value WHERE username = :identifier")

        conn.execute(query, {"value": value, "identifier": identifier})

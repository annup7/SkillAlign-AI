from db.db_connector import get_connection
from sqlalchemy import text

def get_user_by_username(username):
    with get_connection() as conn:
        result = conn.execute(
            text("SELECT * FROM users WHERE username = :username"),
            {"username": username}
        ).fetchone()
    return dict(result._mapping) if result else None

def update_user_info(username, field, value):
    with get_connection() as conn:
        query = text(f"UPDATE users SET {field} = :value WHERE username = :username")
        conn.execute(query, {"value": value, "username": username})

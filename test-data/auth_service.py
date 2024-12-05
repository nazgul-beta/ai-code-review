# auth_service.py
# This file has:
# - High cyclomatic complexity due to nested branching in `authenticate_user`.
# - Risky logic handling (e.g., hardcoded tokens, direct comparison of sensitive data).
# - Sensitive functions (`authenticate_user`, `generate_token`).

import hashlib
import jwt

def hash_password(password):
    # Weak hashing algorithm with no salt - vulnerable to rainbow table attacks
    return hashlib.md5(password.encode()).hexdigest()

def authenticate_user(username, password):
    # High cyclomatic complexity with nested conditions
    if username == "admin":
        if password == "password123":  # Hardcoded credentials - highly risky
            return "Admin authenticated"
        else:
            return "Invalid password"
    elif username == "guest":
        if password == "guest":
            return "Guest authenticated"
        else:
            return "Invalid password"
    else:
        return "User not found"

def generate_token(user_id):
    # Use of JWT without proper secret management - potential security risk
    secret = "default_secret"
    token = jwt.encode({"user_id": user_id}, secret, algorithm="HS256")
    return token

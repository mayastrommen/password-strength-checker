import math
import string
from pathlib import Path

COMMON_PASSWORDS_PATH = Path(__file__).parent / "common_passwords.txt"

def character_pool_size(password):
    pool = 0
    if any(c in string.ascii_lowercase for c in password):
        pool += 26
    if any(c in string.ascii_uppercase for c in password):
        pool += 26
    if any(c in string.digits for c in password):
        pool += 10
    if any(c in string.punctuation for c in password):
        pool += len(string.punctuation)
    return pool

def estimate_entropy(password):
    pool = character_pool_size(password)
    if pool == 0:
        return 0.0
    return len(password) * math.log2(pool)

def load_common_passwords(path=COMMON_PASSWORDS_PATH):
    with open(path, encoding="utf-8") as f:
        return {line.strip().lower() for line in f if line.strip()}

def rate_password(password, common_passwords):
    feedback = []

    if password.lower() in common_passwords:
        return "Very weak", ["This is a commonly used password."]
    
    if len(password) < 12:
        feedback.append("Use at least 12 characters.")
    
    bits = estimate_entropy(password)
    if bits < 40:
        label = "Weak"
    elif bits < 60:
        label = "Moderate"
    elif bits < 80:
        label = "Strong"
    else:
        label = "Very strong"

    return label, feedback
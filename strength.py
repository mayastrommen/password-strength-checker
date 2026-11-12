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

def has_repeated_run(password, run_length=3):
    count = 1
    for i in range(1, len(password)):
        if password[i] == password[i - 1]:
            count += 1
            if count >= run_length:
                return True
        else:
            count = 1
    return False

def has_sequence(password, seq_length=4):
    lowered = password.lower()
    for i in range(len(lowered) - seq_length + 1):
        chunk = lowered[i:i + seq_length]
        if not chunk.isalnum():
            continue
        steps = [ord(chunk[j + 1]) - ord(chunk[j]) for j in range(seq_length - 1)]
        if all(s == 1 for s in steps) or all(s == -1 for s in steps):
            return True
    return False

def rate_password(password, common_passwords):
    feedback = []

    if password.lower() in common_passwords:
        return "Very weak", ["This is a commonly used password."]

    if len(password) < 12:
        feedback.append("Use at least 12 characters.")

    bits = estimate_entropy(password)

    if has_repeated_run(password):
        bits -= 15
        feedback.append("Avoid repeating the same character 3+ times in a row.")

    if has_sequence(password):
        bits -= 15
        feedback.append("Avoid sequences like abcd or 1234.")

    if bits < 40:
        label = "Weak"
    elif bits < 60:
        label = "Moderate"
    elif bits < 80:
        label = "Strong"
    else:
        label = "Very strong"

    return label, feedback
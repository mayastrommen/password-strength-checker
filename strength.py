import math
import string

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
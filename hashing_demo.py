import hashlib
import os
import time

PBKDF2_ITERATIONS = 600_000

def hash_password(password, salt = None):
    """Return (salt, digest) using PBKDF2-HMAC-SHA256."""
    if salt is None:
        salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS
    )
    return salt, digest

def md5_hash(password):
    """Unsalted MD5" SHown to demonstrate why NOT to use it."""
    return hashlib.md5(password.encode("utf-8")).hexdigest()

def main():
    password = "correct horse battery staple"

    print("=== 1. Unsalted MD5: same input, same output ===")
    print(md5_hash(password))
    print(md5_hash(password))
    print("Identical hashes reveal identical passwords, and precomputed")
    print("lookup tables (rainbow tables) work against them.\n")

    print("=== 2. Salted PBKDF2: same input, different output ===")
    salt1, digest1 = hash_password(password)
    salt2, digest2 = hash_password(password)
    print(digest1.hex())
    print(digest2.hex())
    print(f"Same password, hashes equal? {digest1 == digest2}\n")

    print("=== 3. Verifying a login attempt ===")
    _, check = hash_password(password, salt1)
    print(f"Correct password matches: {check == digest1}")
    _, wrong = hash_password("wrong guess", salt1)
    print(f"Wrong password matches:   {wrong == digest1}\n")

    print("=== 4. Speed comparison ===")
    start = time.perf_counter()
    for _ in range(100):
        md5_hash(password)
    md5_time = (time.perf_counter() - start) / 100

    start = time.perf_counter()
    hash_password(password)
    pbkdf2_time = time.perf_counter() - start

    print(f"MD5:    {md5_time * 1000:.4f} ms per hash")
    print(f"PBKDF2: {pbkdf2_time * 1000:.1f} ms per hash")
    print("PBKDF2 is slow on purpose: it makes each guess expensive for")
    print("an attacker trying billions of passwords.")


if __name__ == "__main__":
    main()
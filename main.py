from getpass import getpass

from strength import estimate_entropy, load_common_passwords, rate_password


def main():
    common = load_common_passwords()
    password = getpass("Enter a password to check: ")

    if not password:
        print("No password entered.")
        return

    label, feedback = rate_password(password, common)
    bits = estimate_entropy(password)

    print(f"Rating: {label} (~{bits:.0f} bits of entropy)")
    for tip in feedback:
        print(f"- {tip}")


if __name__ == "__main__":
    main()
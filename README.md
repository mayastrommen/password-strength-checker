# Password Strength Checker

A command-line tool, built in python, that estimates how strong a password is, plus a demo of why passwords should be stored with salted, slow hashes.

## Features

- Estimates password entropy using length and character variety
- Checks against a list of 1,000 common passwords
- Flags repeated or sequential characters ('aaa', '1234')
- Returns rating and feedback, based on input
- Reads input with 'getpass' to hide password on screen
- Includes demo for hashing, comparing unsalted MD5 with salted PBKDF2-HMAC-SHA256

## Usage
'''bash
git clone https://github.com/YOUR-USERNAME/password-strength-checker.git
cd password-strength-checker
python3 -m venv venv
source venv/bin/activate
pip install pytest

python3 main.py          # check a password
python3 hashing_demo.py  # run the hashing demo
pytest -v                # run the tests
'''

Example Output:

'''
Rating: Weak (~35 bits of entropy)
Use at least 12 characters.
'''

## How it works

**Entropy:** estimated using 'length x log2(character pool size)', where the pool 
is the combined size of the character types used (lowercase, uppercase, digits,
symbols).

**Pattern penalties:** 15 bits are subtracted for a repeated run and 15 extra for a sequence.

**Ratings:** under 40 bits is Weak, 40 to 59 is Moderate, 60 to 79 is Strong, and 80+ is Very Strong. Anything shown on the common-password list is Very Weak.

**Hashing demo:** shows that unsalted MD5 gives identical output for identical input(not recommended), while salted PBKDF2 (600,000 iterations, per OWASP's Password Storage Cheat Sheet) gives a different hash each time and is deliberatley slow to make brute force password guessing expensive.

## Limitations

- Entropy is an estimate, so the thresholds and 15-bit penalties are heuristics that I chose, not industry standard.-
- It assumes passwords are random characters, so it overrates passphrases made of common words.
- The common password list only has 1,000 entries 
- The hashing demo compares hashes with '==", where production code should use 'hmac.compare_digest' to avoid timing attacks.

## Improvements

- Check passwords against larger password database (Could use 'Have I Been Pwned API)
- Detect keyboard patterns and/or common substitutions for characters
- Add 'argparse' options and better/more in depth scoring model

## Learned/New to me

- How entropy was used to detect password strength
- Hashing and salted vs. unsalted for more in-depth storage, as well as stragtegies to protect user info

## Safety Note

Use made-up passwords while testing. This tool does not store or transmit data typed, but best practice to avoid personal information.
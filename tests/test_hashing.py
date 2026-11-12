import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from hashing_demo import hash_password, md5_hash


def test_md5_is_deterministic():
    assert md5_hash("test") == md5_hash("test")


def test_different_salts_give_different_hashes():
    _, digest1 = hash_password("test")
    _, digest2 = hash_password("test")
    assert digest1 != digest2


def test_same_salt_verifies_correctly():
    salt, digest = hash_password("test")
    _, check = hash_password("test", salt)
    assert check == digest


def test_wrong_password_does_not_verify():
    salt, digest = hash_password("test")
    _, check = hash_password("wrong", salt)
    assert check != digest
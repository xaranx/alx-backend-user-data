#!/usr/bin/env python3
"""`encrypt_password.py` contains a hash_password function."""

import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password, which is a byte string."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """returns a boolean indicating whether or not the provided password
    matches the hashed password."""
    return bcrypt.checkpw(password.encode(), hashed_password)


if __name__ == "__main__":
    password = "MyAmazingPassw0rd"
    hashed_password = hash_password(password)
    print(hashed_password)
    print(is_valid(hashed_password, password))

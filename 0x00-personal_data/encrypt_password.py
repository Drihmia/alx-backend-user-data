#!/usr/bin/env python3
""" Encrypt password using the crypt module """
import bcrypt


# Task 5:
def hash_password(password: str) -> bytes:
    """ Hash a password for the first time """

    # Generate a salt: a random sequence of bytes
    salt = bcrypt.gensalt()

    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(
        password.encode(),
        salt)

    return hashed_password


# Task 6:
def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Check if the password is valid """

    # Check if the password is valid, return True if it is_valid
    # otherwise return False
    return bcrypt.checkpw(
        password.encode(),
        hashed_password)

#!/usr/bin/env python3
""" Encrypt password using the crypt module """
import bcrypt


def hash_password(password: str) -> bytes:
    """ Hash a password for the first time """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(b'password', salt)
    return hashed_password

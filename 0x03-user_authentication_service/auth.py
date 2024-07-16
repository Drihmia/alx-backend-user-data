#!/usr/bin/env python3
""" This module provides a simple authentication mechanism for the
    application.
"""
import bcrypt
from db import DB
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from user import User


def _hash_password(password: str) -> bytes:
    """Return password hashed
    """
    if not password:
        return b''
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def _generate_uuid() -> str:
    """Generate a new UUID.
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize the Auth class.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user with the provided email and password.
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except (InvalidRequestError, NoResultFound):
            pass

        hashed_password = _hash_password(password)
        registred_user = self._db.add_user(email, hashed_password)

        return registred_user

    def valid_login(self, email: str, password: str) -> bool:
        """Check if the provided email and password are valid.
        """
        if not email or not password:
            return False

        try:
            user = self._db.find_user_by(email=email)
            if user:
                return bcrypt.checkpw(password.encode(), user.hashed_password)
            return False
        except (InvalidRequestError, NoResultFound):
            return False

    def create_session(self, email: str) -> str:
        """Create a new session for the provided email.
        """
        if not email:
            return None

        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = _generate_uuid()
                self._db.update_user(user.id, session_id=session_id)
                return session_id
            return None

        except (InvalidRequestError, NoResultFound):
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Get a user from the provided session ID.
        """
        if not session_id:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            if user:
                return user
            return None
        except (InvalidRequestError, NoResultFound):
            return None

    def destroy_session(self, user_id: int):
        """Destroy the session for the provided user ID.
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Get a reset password token for the provided email.
        """
        if not email:
            raise ValueError

        user = self._db.find_user_by(email=email)
        if not user:
            raise ValueError
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str):
        """Update the password for the provided reset token.
        """
        user = self._db.find_user_by(reset_token=reset_token)
        if not user:
            raise ValueError
        hashed_password = _hash_password(password)
        self._db.update_user(
            user.id,
            hashed_password=hashed_password,
            reset_token=None
        )
        return None

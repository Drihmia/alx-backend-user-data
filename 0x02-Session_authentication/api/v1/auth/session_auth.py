#!/usr/bin/env python3
""" This module provides a SessionAuth class that inherite from Auth class. """
from .auth import Auth
from models.user import User
import uuid
from typing import TypeVar
from os import getenv


class SessionAuth(Auth):
    """ SessionAuth class that inherite from Auth class. """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ A method that creates a session ID for user_id.
        Args:
            user_id (str): A string representing the user ID.
        Returns:
            session_id (str): A string representing the session ID.
            otherwise, return None.
        """
        if not user_id:
            return None

        if type(user_id) is not str:
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id.update({session_id: user_id})

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ A method that returns a User ID based on a Session ID.
        Args:
            session_id (str): A string representing the Session ID.
        Returns:
            user_id (str): A string representing the User ID.
            otherwise, return None.
        """
        if not session_id:
            return None

        if type(session_id) is not str:
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """ A method that returns a User instance based on a cookie value.
        Args:
            request (Request): A Request object.
        Returns:
            user (User): A User instance.
            otherwise, return None.
        """
        session_id = self.session_cookie(request)
        # print("session ID from session auth:\n", session_id)

        if not session_id:
            return None

        user_id = self.user_id_for_session_id(session_id)

        if not user_id:
            return None
        user = User.get(user_id)

        return user

    def destroy_session(self, request=None) -> bool:
        """ A method that deletes the user session / logout.
        Args:
            request (Request): A Request object.
        Returns:
            True: If the session was deleted successfully.
            otherwise, return False.
        """
        if not request:
            return False

        session_name = getenv("SESSION_NAME")
        if session_name == "":
            return False

        session_id = self.session_cookie(request)

        if not session_id:
            return False

        if not self.user_id_for_session_id(session_id):
            return False

        del self.user_id_by_session_id[session_id]

        return True

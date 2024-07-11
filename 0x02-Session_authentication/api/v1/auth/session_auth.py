#!/usr/bin/env python3
""" This module provides a SessionAuth class that inherite from Auth class. """
from .auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """ SessionAuth class that inherite from Auth class. """
    user_id_by_session_id: dict[str, str] = {}

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

    def current_user(self, request=None):
        """ A method that returns a User instance based on a cookie value.
        Args:
            request (Request): A Request object.
        Returns:
            user (User): A User instance.
            otherwise, return None.
        """
        session_id = self.session_cookie(request)

        if not session_id:
            return None

        user_id = self.user_id_by_session_id.get(session_id)

        if not user_id:
            return None

        user = User.get(user_id)

        return user

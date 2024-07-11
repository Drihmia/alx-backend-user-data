#!/usr/bin/env python3
"""
This module provides a class for managing session database authentication.
"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from uuid import uuid4
from os import getenv


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class.
    """
    def create_session(self, user_id=None):
        """
        Creates a new session for a user.
        """
        if not user_id:
            return None
        if type(user_id) is not str:
            return None

        session_id = str(uuid4())
        user_session = UserSession(**{
            "session_id": session_id,
            "user_id": user_id
        })
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns a User ID based on a Session ID.
        """
        super().user_id_for_session_id(session_id)
        if not session_id:
            return None
        if type(session_id) is not str:
            return None

        users_session = UserSession.search({"session_id": session_id})
        if not users_session:
            return None

        user_session = users_session[0]

        user_id = user_session.user_id
        return user_id

    def destroy_session(self, request=None):
        """
        Destroys a session.
        """
        if not request:
            return None

        session_name = getenv("SESSION_NAME")
        cookies = request.cookies

        session_id = cookies.get(session_name)

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return None

        user = UserSession.get(user_id)

        users_session = UserSession.search({"session_id": session_id})
        if not users_session:
            return None

        user_session = users_session[0]
        user_session.remove()

        return True

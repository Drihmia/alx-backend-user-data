#!/usr/bin/env python3
"""
This module provides a class for managing session database authentication.
"""
from os import getenv
from uuid import uuid4
from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth
from typing import TypeVar
from models.user import User
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class.
    """

    def create_session(self, user_id=None) -> str:
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

    def user_id_for_session_id(self, session_id=None) -> str:
        """
        Return the user_id by requesting it from the user_id_by_session_id
        dictionary.
        """
        if not session_id:
            return None

        UserSession.load_from_file()

        # Get session dictionary from user_id_by_session_id dictionary.
        user_sessions = UserSession.search({"session_id": session_id})
        if not user_sessions:
            return None

        user_session = user_sessions[0]

        if self.session_duration <= 0:
            return user_session.user_id

        if (user_session.created_at +
                timedelta(seconds=self.session_duration) < datetime.utcnow()):
            return None

        user_id = user_session.user_id
        return user_id

    def destroy_session(self, request=None) -> bool:
        """
        Destroys a session.
        """

        if not request:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        users_session = UserSession.search({"session_id": session_id})
        if not users_session:
            return False

        user_session = users_session[0]
        user_session.remove()

        return True

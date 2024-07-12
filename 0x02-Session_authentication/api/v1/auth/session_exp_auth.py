#!/usr/bin/env python3
"""
This module contains the SessionExpAuth class
"""
from .session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta
from models.user_session import UserSession


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class
    """
    def __init__(self):
        try:
            self.session_duration = int(getenv("SESSION_DURATION", 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None) -> str:
        """
        Create a new session
        """
        # create a new session id using the super class method.
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session_dictionary = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id.update({session_id: session_dictionary})
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """
        Return the user_id by requesting it from the user_id_by_session_id
        dictionary.
        """
        if not session_id:
            return None
        if session_id not in self.user_id_by_session_id:
            return None

        # Get session dictionary from user_id_by_session_id dictionary.
        session_dictionary = self.user_id_by_session_id.get(session_id, {})
        if not session_dictionary:
            return None

        if self.session_duration <= 0:
            return session_dictionary.get("user_id")

        if "created_at" not in session_dictionary:
            return None
        if (session_dictionary.get("created_at") +
                timedelta(seconds=self.session_duration) < datetime.now()):
            return None
        user_id = session_dictionary.get("user_id")
        return user_id

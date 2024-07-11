#!/user/bin/env python3
"""
This module contains the UserSession class.
"""
from .base import Base


class UserSession(Base):
    """ UserSession class
    """
    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a User's session
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")

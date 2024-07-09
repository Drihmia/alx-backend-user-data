#!/usr/bin/env python3
"""
This module provides a simple authentication mechanism for the application.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ This class is a template for the authentication mechanism. """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ This method checks if the path requires authentication. """
        if not path:
            return True
        if not excluded_paths or not len(excluded_paths):
            return True

        if path[-1] != '/':
            path += '/'

        for excluded_path in excluded_paths:
            if path.startswith(excluded_path.split('*')[0]):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ This method returns the value of the Authorization
        header in the request.
        """
        if not request:
            return None

        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """ This method retrieves the current user. """
        return None

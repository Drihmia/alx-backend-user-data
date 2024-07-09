#!/usr/bin/env python3
""" Basic Auth """
from api.v1.auth.auth import Auth
import base64
import binascii


class BasicAuth(Auth):
    """ Basic Auth inherite from Auth class.
    """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """ A method that returns the Base64 part of the Authorization
        header for a Basic Authentication.
        """
        if not authorization_header:
            return None

        if type(authorization_header) is not str:
            return None

        if not authorization_header.startswith("Basic "):
            return None

        auth_arr = authorization_header.split(" ")
        if len(auth_arr) > 1:
            return auth_arr[1]
        return None

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """ A method that returns the decoded value of a Base64 string.
        """
        if not base64_authorization_header:
            return None

        if type(base64_authorization_header) is not str:
            return None

        try:
            decoded_auth_head = base64.b64decode(base64_authorization_header)
            return decoded_auth_head.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

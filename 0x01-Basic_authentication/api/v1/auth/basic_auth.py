#!/usr/bin/env python3
""" Basic Auth """
from api.v1.auth.auth import Auth
from models.user import User
from base64 import b64decode
from binascii import Error
from typing import TypeVar


class BasicAuth(Auth):
    """ Basic Auth inherite from Auth class.
    """

    def extract_base64_authorization_header(self, authorization_header: str
                                            ) -> str:
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

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """ A method that returns the decoded value of a Base64 string.
        """
        if not base64_authorization_header:
            return None

        if type(base64_authorization_header) is not str:
            return None

        try:
            decoded_auth_head = b64decode(
                base64_authorization_header, validate=True)
            return decoded_auth_head.decode('utf-8')
        except (Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """ A method that returns the user email and password from the Base64
        decoded value.
        """
        if not decoded_base64_authorization_header:
            return None, None

        if type(decoded_base64_authorization_header) is not str:
            return None, None

        if ":" not in decoded_base64_authorization_header:
            return None, None

        credentials = decoded_base64_authorization_header.split(":")

        try:
            return credentials[0], credentials[1]
        except IndexError:
            return None, None

    def user_object_from_credentials(self, user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """ A method that returns the User instance based on his email and
        password.
        """
        if not user_email or type(user_email) is not str:
            return None

        if not user_pwd or type(user_pwd) is not str:
            return None

        user_list = User.search({"email": user_email})
        if not len(user_list):
            return None

        user = user_list[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """ A method that overloads Auth and retrieves the User instance for
        a request.
        """
        auth_body = super().authorization_header(request)

        if not auth_body:
            return None

        auth_token = self.extract_base64_authorization_header(auth_body)
        if not auth_token:
            return None

        decoded_token = self.decode_base64_authorization_header(auth_token)
        if not decoded_token:
            return None

        user_email, user_pwd = self.extract_user_credentials(decoded_token)
        if not user_email or not user_pwd:
            return None
        return self.user_object_from_credentials(user_email, user_pwd)

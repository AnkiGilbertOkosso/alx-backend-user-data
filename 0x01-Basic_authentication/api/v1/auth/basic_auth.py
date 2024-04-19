#!/usr/bin/env python3
"""Basic authentication module.
"""
import base64
import binascii
import re

from models.user import User
from .auth import Auth


class BasicAuth(Auth):
    """Basic authentication class.
    """
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """Extract Base64 Authorization Header

        Extracts the Base64 part of the Authorization header for
        Basic Authentication.

        Args:
            authorization_header (str): The Authorization header string.

        Returns:
            str: The Base64 part of the Authorization header if present,
            otherwise None.
        """
        if type(authorization_header) == str:
            pattern = r'Basic (?P<token>.+)'
            field_match = re.fullmatch(pattern, authorization_header.strip())
            if field_match is not None:
                return field_match.group('token')
        return None

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """Decode Base64 Authorization Header

        Decodes a base64-encoded authorization header.

        Args:
            base64_authorization_header (str): The base64-encoded
            authorization header.

        Returns:
            str: The decoded string if decoding is successful,
            otherwise None.
        """
        if type(base64_authorization_header) == str:
            try:
                response = base64.b64decode(
                    base64_authorization_header,
                    validate=True,
                )
                return response.decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                return None

    from typing import Tuple, TypeVar

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """Extract User Credentials

        Extracts user credentials from a base64-decoded authorization header
        that uses the Basic authentication flow.

        Args:
            decoded_base64_authorization_header (str): The decoded base64
            authorization header.

        Returns:
            Tuple[str, str]: A tuple containing the extracted
            username and password.
                If extraction fails, returns (None, None).
        """
        if type(decoded_base64_authorization_header) == str:
            pattern = r'(?P<user>[^:]+):(?P<password>.+)'
            field_match = re.fullmatch(
                pattern,
                decoded_base64_authorization_header.strip(),
            )
            if field_match is not None:
                user = field_match.group('user')
                password = field_match.group('password')
                return user, password
        return None, None

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):  # type: ignore
        """Retrieve User Object from Credentials

        Retrieves a user based on the user's authentication credentials.

        Args:
            user_email (str): The email address of the user.
            user_pwd (str): The password of the user.

        Returns:
            TypeVar('User'): The user object if authentication is successful,
            otherwise None.
        """
        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """Retrieve Current User from Request
        
        Retrieves the user from a request.

        Args:
            request (Request): The Flask request object. Defaults to None.

        Returns:
            TypeVar('User'): The user object if authentication is successful,
            otherwise None.
        """
        auth_header = self.authorization_header(request)
        bs64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(bs64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)
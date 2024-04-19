#!/usr/bin/env python3
"""Authentication Module

Provides functionalities for authentication in the API.
"""
import re
from typing import List, TypeVar
from flask import request


class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if Path Requires Authentication

        Args:
            path (str): The path to check for authentication.
            excluded_paths (List[str]): List of paths excluded
            from authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """

        return False

    def authorization_header(self, request=None) -> str:
        """Get Authorization Header Field

        Args:
            request (Request): The request object.

        Returns:
            str: The authorization header field from the request.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """Get Current User

        Args:
            request (Request): The request object.

        Returns:
            TypeVar('User'): The current user from the request.
        """
        return None

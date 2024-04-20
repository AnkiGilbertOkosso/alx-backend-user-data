#!/usr/bin/env python3
"""Session Authentication Module

Provides session authentication functionality for the API.
"""
from uuid import uuid4
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """Session Authentication Class"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create Session

        Creates a session ID for the user.

        Args:
            user_id (str): The user ID associated with the session.

        Returns:
            str: The generated session ID.
        """
        if type(user_id) is str:
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """User ID for Session ID

        Retrieves the user ID associated with a given session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            str: The user ID associated with the session ID.
        """
        if type(session_id) is str:
            return self.user_id_by_session_id.get(session_id)

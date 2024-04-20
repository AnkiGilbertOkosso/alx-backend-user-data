#!/usr/bin/env python3
"""Session Authentication with Expiration Module

Provides session authentication functionality with expiration for the API.
"""
import os
from flask import request
from datetime import datetime, timedelta

from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session Authentication Class with Expiration"""

    def __init__(self) -> None:
        """Initialize SessionExpAuth instance."""
        super().__init__()
        try:
            self.duration_of_session = int(os.getenv('SESSION_DURATION', '0'))
        except Exception:
            self.duration_of_session = 0

    def create_session(self, user_id=None):
        """Create Session

        Creates a session ID for the user.

        Returns:
            str: The generated session ID if successful, otherwise None.
        """
        session_id = super().create_session(user_id)
        if type(session_id) != str:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """User ID for Session ID

        Retrieves the user ID associated with a given session ID.

        Returns:
            str: The user ID associated with the session ID.
        """
        if session_id in self.user_id_by_session_id:
            session_dict = self.user_id_by_session_id[session_id]
            if self.duration_of_session <= 0:
                return session_dict['user_id']
            if 'created_at' not in session_dict:
                return None
            current_time = datetime.now()
            time_span = timedelta(seconds=self.duration_of_session)
            expiration_time = session_dict['created_at'] + time_span
            if expiration_time < current_time:
                return None
            return session_dict['user_id']

#!/usr/bin/env python3
"""Session Authentication with Expiration and Storage Support Module

Provides session authentication functionality with expiration
and storage support for the API.
"""
from flask import request
from datetime import datetime, timedelta

from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """Session Authentication Class with Expiration and Storage Support"""

    def create_session(self, user_id=None) -> str:
        """Create and Store Session

        Creates and stores a session ID for the user.

        Returns:
            str: The generated session ID if successful, otherwise None.
        """
        session_id = super().create_session(user_id)
        if type(session_id) == str:
            kwargs = {
                'user_id': user_id,
                'session_id': session_id,
            }
            user_session = UserSession(**kwargs)
            user_session.save()
            return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """User ID for Session ID

        Retrieves the user ID associated with a given session ID.

        Returns:
            str: The user ID associated with the session ID.
        """
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        cur_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        exp_time = sessions[0].created_at + time_span
        if exp_time < cur_time:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None) -> bool:
        """Destroy Session

        Destroys an authenticated session.

        Returns:
            bool: True if the session was successfully destroyed, False
            otherwise.
        """
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        sessions[0].remove()
        return True

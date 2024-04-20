#!/usr/bin/env python3
"""Session Authentication Views Module

Provides views for session authentication in the API.
"""
import os
from typing import Tuple
from flask import abort, jsonify, request

from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """User Login - POST /api/v1/auth_session/login

    Log in a user with session authentication.

    Returns:
        Tuple[str, int]: JSON representation of a User object and status code.
    """
    not_found_response = {"error": "no user found for this email"}
    email = request.form.get('email')
    if email is None or len(email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password is None or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify(not_found_response), 404
    if len(users) <= 0:
        return jsonify(not_found_response), 404
    if users[0].is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(getattr(users[0], 'id'))
        response = jsonify(users[0].to_json())
        response.set_cookie(os.getenv("SESSION_NAME"), session_id)
        return response
    return jsonify({"error": "wrong password"}), 401


@app_views.route(
    '/auth_session/logout',
    methods=['DELETE'],
    strict_slashes=False)
def logout() -> Tuple[str, int]:
    """User Logout - DELETE /api/v1/auth_session/logout

    Log out a user with session authentication.

    Returns:
        Tuple[str, int]: An empty JSON object and status code.
    """
    from api.v1.app import auth
    is_destroyed = auth.destroy_session(request)
    if not is_destroyed:
        abort(404)
    return jsonify({})

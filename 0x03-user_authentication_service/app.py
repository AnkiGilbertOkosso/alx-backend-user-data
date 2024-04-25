#!/usr/bin/env python3
"""Basic Flask app
"""
from flask import Flask, jsonify, request

from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """GET /
    Return:
        - The home pages.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """Handle user registration."""
    email, password = request.form.get("email"), request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "User created"}), 200
    except ValueError:
        return jsonify({"message": "Email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

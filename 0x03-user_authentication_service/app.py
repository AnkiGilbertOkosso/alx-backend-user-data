#!/usr/bin/env python3
"""Basic Flask app
"""
from flask import Flask, jsonify, request, abort, Response, redirect

from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> Response:
    """GET /
    Return:
        - The home pages.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> Response:
    """Handle user registration."""
    if request.method == "POST":
        r_email = request.form.get("email")
        email = r_email.strip()
        r_password = request.form.get("password")
        password = r_password.strip()
        try:
            AUTH.register_user(email, password)
            return jsonify({"email": email, "message": "User created"})
        except Exception:
            return jsonify({"message": "Email already registered"})
    else:
        abort(400)


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """POST /sessions
    """
    email, password = request.form.get("email"), request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    id = AUTH.create_session(email)
    res = jsonify({"email": email, "message": "logged in"})
    res.set_cookie("session_id", id)
    return res


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """DELETE /sessions
    """
    id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """GET /profile
    """
    id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

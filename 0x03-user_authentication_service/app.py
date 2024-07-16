#!/usr/bin/env python3
"""
This is a simple web application that uses the Flask framework.
"""
from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def welcome():
    """A simple route that returns welcome in Frensh
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["GET", "POST"], strict_slashes=False)
def users():
    """Register a user in database
    """

    email = request.form.get("email")
    password = request.form.get("password")

    try:
        registred_user = AUTH.register_user(email, password)
        return jsonify({
            "email": registred_user.email,
            "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["GET", "POST"], strict_slashes=False)
def login():
    """Login a user
    """

    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        abort(401)

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)

    resp = jsonify({"email": email, "message": "logged in"})
    resp.set_cookie("session_id", session_id)
    return resp


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """Logout a user
    """
    cookies = request.cookies
    session_id = cookies.get("session_id")
    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    resp_red = redirect(url_for('welcome'))
    # resp_red.set_cookie("session_id", "")
    resp_red.delete_cookie("session_id")
    return resp_red


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

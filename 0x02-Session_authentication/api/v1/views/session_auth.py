#!/usr/bin/env python3
"""
This module provides a class for managing session authentication.
"""
from flask import request, jsonify
from os import getenv
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def auth_session():
    print("form data: ", request.form)
    email = request.form.get("email", "")
    password = request.form.get("password", "")

    if email == '':
        return jsonify({"error": "email missing"}), 400

    if password == '':
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})

    if not len(users):
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    resp = jsonify(user.to_json())

    from api.v1.app import auth

    session = auth.create_session(user.id)

    session_name = getenv('SESSION_NAME')
    resp.set_cookie(session_name, session)

    return resp

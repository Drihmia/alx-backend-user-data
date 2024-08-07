#!/usr/bin/env python3
"""
This module provides a class for managing session authentication.
"""
from flask import request, jsonify, abort
from os import getenv
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def auth_session():
    """
    POST /auth_session/login
    """

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

    from api.v1.app import auth

    session_id = auth.create_session(user.id)

    resp = jsonify(user.to_json())

    session_name = getenv('SESSION_NAME')
    resp.set_cookie(session_name, session_id)

    return resp


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """
    DELETE /auth_session/logout
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)

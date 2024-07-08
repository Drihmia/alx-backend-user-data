#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, Response
from flask_cors import (CORS, cross_origin)
import os
from typing import Tuple, Dict


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
auth_env = getenv("AUTH_TYPE")

if auth_env == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif auth_env == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


@app.errorhandler(404)
def not_found(error) -> Tuple[Response, int]:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> Tuple[Response, int]:
    """Not authorized requests
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> Tuple[Response, int]:
    """ Not allowed requests
    """
    return jsonify({
        "error": "Forbidden"
    }), 403


@app.before_request
def filter():
    """ Filter incoming requests.
    """
    if not auth:
        return

    exc_list = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/'
    ]

    path = str(request.path)

    if not auth.require_auth(path, exc_list):
        return

    if not auth.authorization_header(request):
        abort(401)

    if not auth.current_user(request):
        abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    try:
        port_str = getenv("API_PORT", "5000")
        port = int(port_str)
    except ValueError:
        port = 5000
    app.run(host=host, port=port)

#!/usr/bin/env python3
"""
Main file
"""
from requests import get, post, delete, put


def register_user(email: str, password: str) -> None:
    """
    Test  /users endpoint
    """
    endpoint = 'users'
    form = {"email": EMAIL, "password": PASSWD}

    resp = post(
        base_url + endpoint,
        data=form
    )

    expected_resp = {
        'email': 'guillaume@holberton.io',
        'message': 'user created'
    }

    assert resp.status_code == 200

    Content_Type = resp.headers.get('Content-Type')
    assert Content_Type is not None
    assert 'json' in Content_Type
    assert resp.json() == expected_resp


def log_in_wrong_password(email: str, password: str) -> None:
    endpoint = 'sessions'
    form = {"email": "wrong@email", "password": "wrong pwd"}

    resp = post(
        base_url + endpoint,
        data=form
    )

    assert resp.status_code == 401
    assert "401 Unauthorized" in resp.text


def log_in(email: str, password: str) -> str:
    endpoint = 'sessions'
    form = {"email": email, "password": password}

    resp = post(
        base_url + endpoint,
        data=form
    )

    expected_resp = {
        'email': EMAIL,
        'message': 'logged in'
    }
    session_id = resp.cookies.get("session_id")

    assert resp.status_code == 200

    Content_Type = resp.headers.get('Content-Type')
    assert Content_Type is not None
    assert 'json' in Content_Type
    assert resp.json() == expected_resp
    assert session_id is not None
    assert len(session_id) == 36

    return session_id


def profile_unlogged() -> None:
    endpoint = 'profile'
    cookies = {"session_id": "wrong session ID"}

    resp = get(
        base_url + endpoint,
        cookies=cookies
    )

    assert resp.status_code == 403
    assert "403 Forbidden" in resp.text


def profile_logged(session_id: str) -> None:
    endpoint = 'profile'
    cookies = {"session_id": session_id}

    resp = get(
        base_url + endpoint,
        cookies=cookies
    )

    assert resp.status_code == 200

    Content_Type = resp.headers.get('Content-Type')
    assert Content_Type is not None
    assert 'json' in Content_Type
    assert resp.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    endpoint = 'sessions'
    cookies = {"session_id": session_id}

    resp = delete(
        base_url + endpoint,
        cookies=cookies
    )

    assert resp.status_code == 200

    Content_Type = resp.headers.get('Content-Type')
    assert Content_Type is not None
    assert 'json' in Content_Type
    assert resp.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    endpoint = 'reset_password'
    resp = post(
        base_url + endpoint,
        data={'email': email}
    )

    assert resp.status_code == 200

    Content_Type = resp.headers.get('Content-Type')
    assert Content_Type is not None
    assert 'json' in Content_Type

    resp_json = resp.json()

    assert "email" in resp_json
    assert resp_json.get("email") == email
    assert len(resp_json.get("reset_token", "")) == 36

    return resp_json.get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    endpoint = 'reset_password'
    resp = put(
        base_url + endpoint,
        data={
            'email': email,
            'reset_token': reset_token,
            'new_password': new_password
        }
    )

    assert resp.status_code == 200

    Content_Type = resp.headers.get('Content-Type')
    assert Content_Type is not None
    assert 'json' in Content_Type

    resp_json = resp.json()

    assert resp_json == {"email": email, "message": "Password updated"}


base_url = "http://127.0.0.1:5000/"
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)

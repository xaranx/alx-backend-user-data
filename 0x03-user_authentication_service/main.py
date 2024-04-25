
#!/usr/bin/env python3
"""
Main file
"""
import requests

URL = 'http://localhost:5000'


def register_user(email: str, password: str) -> None:
    """Register a user
    """
    res = requests.post(
        f'{URL}/users', data={'email': email, 'password': password})
    assert res.json() == {'email': email, 'message': 'user created'}


def log_in_wrong_password(email: str, password: str) -> None:
    """Log in with wrong password
    """
    res = requests.post(f'{URL}/sessions',
                        data={'email': email, 'password': password})
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """Log in with correct password
    """
    res = requests.post(f'{URL}/sessions',
                        data={'email': email, 'password': password})
    assert res.json() == {'email': email, 'message': 'logged in'}
    assert res.status_code == 200
    assert res.cookies.get('session_id') is not None
    return res.cookies.get('session_id')


def profile_unlogged() -> None:
    """Profile of a user that is not logged in
    """
    res = requests.get(f'{URL}/profile')
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """Profile of a user that is logged in
    """
    res = requests.get(f'{URL}/profile', cookies={'session_id': session_id})
    assert res.json().get('email') is not None
    assert res.status_code == 200


def log_out(session_id: str) -> None:
    """Log out
    """
    res = requests.delete(
        f'{URL}/sessions', cookies={'session_id': session_id})
    assert res.status_code == 200
    assert res.json() == {'message': 'Bienvenue'}
    assert res.cookies.get('session_id') is None


def reset_password_token(email: str) -> str:
    """Reset password token
    """
    res = requests.post(f'{URL}/reset_password', data={'email': email})
    assert res.status_code == 200
    assert res.json().get('email') == email
    assert res.json().get('reset_token') is not None
    return res.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update password
    """
    res = requests.put(f'{URL}/reset_password',
                       data={'email': email, 'reset_token': reset_token,
                             'new_password': new_password})
    assert res.status_code == 200
    assert res.json() == {'email': email, 'message': 'Password updated'}


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


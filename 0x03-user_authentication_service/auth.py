#!/usr/bin/env python3
"""Auth module defines authentication utilities.
"""
from typing import Optional
import uuid
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user if not exists
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(
                email, _hash_password(password).decode("utf-8"))

        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """Check if credentials match existing user
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        return bcrypt.checkpw(
            password.encode("utf-8"), user.hashed_password.encode("utf-8"))

    def create_session(self, email: str) -> Optional[str]:
        """Create a session for the user
        """
        try:
            user = self._db.find_user_by(email=email)
            sesh_id = _generate_uuid()
            self._db.update_user(user.id, session_id=sesh_id)
        except NoResultFound:
            return None

        return sesh_id

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """Get user by session_id
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """Sets a user's session_id to None
        """
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str):
        """Create a reset_token for the user
        """
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
        except NoResultFound:
            raise ValueError()

        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update a user's password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError()

        hash_pw = _hash_password(password)
        self._db.update_user(
            user.id, hashed_password=hash_pw.decode("utf-8"), reset_token=None)
        return None


def _hash_password(password: str) -> bytes:
    """Hash a password
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a UUID string
    """
    return str(uuid.uuid4())

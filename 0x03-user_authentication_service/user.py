#!/usr/bin/env python3
"""
The model will have the following attributes:

    - id, the integer primary key
    - email, a non-nullable string
    - hashed_password, a non-nullable string
    - session_id, a nullable string
    - reset_token, a nullable string
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import VARCHAR, Column, Integer

Base = declarative_base()


class User(Base):
    """A SQL user class
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(VARCHAR(250), nullable=False)
    hashed_password = Column(VARCHAR(250), nullable=False)
    session_id = Column(VARCHAR(250), nullable=True)
    reset_token = Column(VARCHAR(250), nullable=True)

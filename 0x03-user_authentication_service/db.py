#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email, hashed_password) -> TypeVar('User'):
        """Create new User instance
        """

        user = User(email, hashed_password)

        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> TypeVar('User'):
        """Find user instance by attribute given as keyword-arguments,
        from the first row in the users table satisfy kyargs given.
        """

        # Dynamically listing User's public attributes
        attributes = set(
            attr
            for attr in User.__dict__
            if not attr.startswith("_")
        )

        user: list = []

        for k, v in kwargs.items():
            if k not in attributes:
                raise InvalidRequestError(f"{k} is not a valid attribute")

            attribute = getattr(User, k)
            user = self._session.query(User).filter(attribute == v).first()

            # First instance found shall be returned
            if user:
                return user
        # If no user's instance is found
        if not user:
            raise NoResultFound("No user found")

    def update_user(self, user_id: int, **kwargs):
        """Update a user's instance
        """
        if not user_id:
            raise ValueError("user_id is required")

        user = self._session.query(User).filter(User.id == user_id).first()

        for k, v in kwargs.items():
            if hasattr(user, k):
                setattr(user, k, v)
            else:
                raise ValueError(f"{k} is not a valid attribute")

        self._session.add(user)
        self._session.commit()
        return None
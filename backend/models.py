"""Class for storage of all database models."""

from sqlalchemy import Column, Integer, String, Unicode
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    Class for base users.

    This encompasses teachers, students and parents.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    password = Column(Unicode, nullable=False)
    email = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)

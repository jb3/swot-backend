"""Class for storage of all database models."""

from sqlalchemy import Column, ForeignKey, Integer, String, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import PrimaryKeyConstraint

Base = declarative_base()


class Class(Base):
    """A model representing a teaching group."""

    __tablename__ = "classes"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=False, nullable=False)
    code = Column(String, unique=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="owned_classes")

    members = relationship("ClassMembership", back_populates="cls", cascade="delete")


class User(Base):
    """
    Class for base users.

    This encompasses teachers, students and parents.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    password = Column(Unicode, nullable=False)
    email = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)

    # Classes owned by this user
    owned_classes = relationship(
        "Class",
        order_by=Class.id,
        back_populates="owner",
        cascade="save-update, merge, delete",
    )

    # Classes joined by this user
    classes = relationship("ClassMembership", back_populates="user", cascade="delete",)


class ClassMembership(Base):
    """
    Represents a student account being a member of a class.

    NOTE: The class attribute is named cls to avoid collision with the Python
          keyword class.
    """

    __tablename__ = "memberships"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)

    __table_args__ = (PrimaryKeyConstraint(user_id, class_id), {})

    cls = relationship("Class", back_populates="members")
    user = relationship("User", back_populates="classes")

"""Class for storage of all database models."""
from datetime import date
from enum import Enum

from sqlalchemy import Column, ForeignKey, Integer, String, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy.types import Date
from sqlalchemy.types import Enum as SQLEnum

Base = declarative_base()


class Class(Base):
    """A model representing a teaching group."""

    __tablename__ = "classes"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=False, nullable=False)
    code = Column(String, unique=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="owned_classes")

    members = relationship(
        "ClassMembership",
        back_populates="cls",
        order_by="User.username",
        cascade="delete",
    )

    tasks = relationship(
        "Task", back_populates="cls", order_by="Task.due_at.asc()", cascade="delete",
    )


class UserType(Enum):
    """Enuerable representing a type of user."""

    STUDENT = "student"
    TEACHER = "teacher"
    PARENT = "parent"


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
    type = Column(SQLEnum(UserType), nullable=False)

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


class TaskType(Enum):
    """Enumerable representing the type of an assigned task."""

    HOMEWORK = "homework"
    CLASSWORK = "classwork"
    REVISION = "revision"


class Task(Base):
    """Represents a task within a class which must be completed by students."""

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    type = Column(SQLEnum(TaskType), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    due_at = Column(Date, nullable=False)

    cls = relationship("Class", back_populates="tasks")

    @property
    def formatted_date(self) -> str:
        """Format the date like: dd/mm/yyyy (XX days remaining)."""
        d = self.due_at.date()

        first_comp = d.strftime("%d/%m/%Y")

        left = d - date.today()

        if left.days > 1:
            second_comp = f"in {left.days} days"
        elif left.days < -1:
            second_comp = f"{left.days} ago"
        elif left.days == -1:
            second_comp = "yesterday"
        elif left.days == 1:
            second_comp = "tomorrow"
        else:
            second_comp = "today"

        return f"{first_comp} ({second_comp})"

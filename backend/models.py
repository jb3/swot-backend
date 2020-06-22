"""Class for storage of all database models."""
from datetime import date
from enum import Enum

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Class(db.Model):
    """A model representing a teaching group."""

    __tablename__ = "classes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)
    code = db.Column(db.String, unique=True, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    owner = db.relationship("User", back_populates="owned_classes")

    members = db.relationship("ClassMembership", back_populates="cls", cascade="delete")

    tasks = db.relationship(
        "Task", back_populates="cls", order_by="Task.due_at.asc()", cascade="delete",
    )


class UserType(Enum):
    """Enuerable representing a type of user."""

    STUDENT = "student"
    TEACHER = "teacher"
    PARENT = "parent"


class User(db.Model):
    """
    Class for base users.

    This encompasses teachers, students and parents.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    password = db.Column(db.Unicode, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    type = db.Column(db.Enum(UserType), nullable=False)

    # Classes owned by this user
    owned_classes = db.relationship(
        "Class",
        order_by=Class.id,
        back_populates="owner",
        cascade="save-update, merge, delete",
    )

    # Classes joined by this user
    classes = db.relationship(
        "ClassMembership", back_populates="user", cascade="delete"
    )


class ClassMembership(db.Model):
    """
    Represents a student account being a member of a class.

    NOTE: The class attribute is named cls to avoid collision with the Python
          keyword class.
    """

    __tablename__ = "memberships"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey("classes.id"), nullable=False)

    __table_args__ = (db.PrimaryKeyConstraint(user_id, class_id), {})

    cls = db.relationship("Class", back_populates="members")
    user = db.relationship("User", back_populates="classes")


class TaskType(Enum):
    """Enumerable representing the type of an assigned task."""

    HOMEWORK = "homework"
    CLASSWORK = "classwork"
    REVISION = "revision"


class Task(db.Model):
    """Represents a task within a class which must be completed by students."""

    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey("classes.id"), nullable=False)
    type = db.Column(db.Enum(TaskType), nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    due_at = db.Column(db.Date, nullable=False)

    cls = db.relationship("Class", back_populates="tasks")

    @property
    def formatted_date(self) -> str:
        """Format the date like: dd/mm/yyyy (XX days remaining)."""
        d = self.due_at.date()

        first_comp = d.strftime("%d/%m/%Y")

        left = d - date.today()

        if left.days > 1:
            second_comp = f"in {left.days} days"
        elif left.days < -1:
            second_comp = f"{abs(left.days)} days ago"
        elif left.days == -1:
            second_comp = "yesterday"
        elif left.days == 1:
            second_comp = "tomorrow"
        else:
            second_comp = "today"

        return f"{first_comp} ({second_comp})"

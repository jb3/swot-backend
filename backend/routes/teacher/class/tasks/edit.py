"""A portal for allowing teachers to edit tasks."""
from datetime import date

from flask import Response, abort, g, redirect, render_template, request, url_for

from backend.models import Class, Task, TaskType, UserType
from backend.route import Route
from backend.utils import authenticated


class EditTask(Route):
    """A route for editing tasks."""

    name = "edit"
    path = "/<int:class_id>/edit/<int:task_id>"

    @authenticated(user_type=UserType.TEACHER)
    def get(self, class_id: int, task_id: int) -> Response:  # skipcq: PYL-R0201
        """Display form to the user for task editing."""
        cls = self.sess.query(Class).filter_by(id=class_id).first()
        task = self.sess.query(Task).filter_by(id=task_id, class_id=class_id).first()

        if not cls or not task:
            return abort(404)

        if cls.owner.id != g.user.id:
            return abort(403)

        return render_template(
            "teacher/class/tasks/edit.html", cls=cls, errors={}, task=task
        )

    @authenticated(user_type=UserType.TEACHER)
    def post(self, class_id: int, task_id: int) -> Response:
        """Update attributes of a task."""
        cls = self.sess.query(Class).filter_by(id=class_id).first()
        task = self.sess.query(Task).filter_by(id=task_id, class_id=class_id).first()

        if not cls or not task:
            return abort(404)

        if cls.owner.id != g.user.id:
            return abort(403)

        required_keys = [
            "title",
            "description",
            "due_at[day]",
            "due_at[month]",
            "due_at[month]",
            "type",
        ]

        errors = {}

        for key in required_keys:
            if (
                not request.form.get(key)
                or request.form.get(key) == ""
                or request.form.get(key).isspace()
            ):
                errors[key] = "You must fill out this field"

        if any("due_at" in key for key in errors):
            errors["due_at"] = "You must fill out this field"

        if len(errors) > 0:
            return render_template(
                "teacher/class/tasks/edit.html", cls=cls, errors=errors, task=task
            )

        data = request.form.copy()

        try:
            due_at = date(
                int(data["due_at[year]"].lstrip("0")),
                int(data["due_at[month]"].lstrip("0")),
                int(data["due_at[day]"].lstrip("0")),
            )
        except ValueError:
            errors[
                "due_at"
            ] = "Could not parse date, did you enter the digits correctly?"

        data["type"] = TaskType(data["type"])
        data["due_at"] = due_at

        if len(errors) > 0:
            return render_template(
                "teacher/class/tasks/edit.html", cls=cls, errors=errors, task=task
            )

        for attribute, val in data.items():
            if hasattr(task, attribute):
                setattr(task, attribute, val)

        self.sess.commit()

        return redirect(url_for("teacher/class/tasks.view", class_id=class_id))

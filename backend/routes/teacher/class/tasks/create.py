"""A portal for allowing teachers to create a new tasks."""
from datetime import date

from flask import abort, Response, g, redirect, render_template, request, url_for

from backend.models import Class, Task, TaskType, UserType
from backend.route import Route
from backend.utils import authenticated


class CreateTask(Route):
    """A route for displaying tasks."""

    name = "create"
    path = "/<int:class_id>/create"

    @authenticated(user_type=UserType.TEACHER)
    def get(self, class_id: int) -> Response:  # skipcq: PYL-R0201
        """Display form to the user for task creation."""
        cls = self.sess.query(Class).filter_by(id=class_id).first()

        if not cls:
            return abort(404)

        if cls.owner.id != g.user.id:
            return abort(403)

        return render_template(
            "teacher/class/tasks/create.html", cls=cls, errors={}, state={}
        )

    @authenticated(user_type=UserType.TEACHER)
    def post(self, class_id: int) -> Response:
        """Create a new task with provided data."""
        cls = self.sess.query(Class).filter_by(id=class_id).first()

        if not cls:
            return abort(404)

        print(request.form)

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
                "teacher/class/tasks/create.html",
                cls=cls,
                errors=errors,
                state=request.form,
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

        if len(errors) > 0:
            return render_template(
                "teacher/class/tasks/create.html",
                cls=cls,
                errors=errors,
                state=request.form,
            )

        task = Task(
            cls=cls,
            title=data["title"],
            description=data["description"],
            due_at=due_at,
            type=TaskType(data["type"]),
        )

        self.sess.add(task)
        self.sess.commit()

        return redirect(url_for("teacher/class/tasks.view", class_id=class_id))

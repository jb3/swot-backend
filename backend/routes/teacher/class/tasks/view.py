"""Provide specifics on a class to a teacher."""

from flask import Response, abort, g, render_template, request

from backend.models import Class, Task, UserType
from backend.route import Route
from backend.utils import authenticated


class TaskList(Route):
    """A route for displaying classes."""

    name = "view"
    path = "/<int:class_id>"

    @authenticated(user_type=UserType.TEACHER)  # skipcq: PYL-R0201s
    def get(self, class_id: int) -> Response:
        """Display a task page to the teachers."""
        cls = Class.query.filter_by(id=class_id).first()

        if not cls:
            return abort(404)

        if cls.owner.id != g.user.id:
            return abort(403)

        return render_template("teacher/class/tasks/view.html", cls=cls)

    @authenticated(user_type=UserType.TEACHER)
    def delete(self, class_id: int) -> Response:
        """Remove a task from a class."""
        cls = Class.query.filter_by(id=class_id).first()

        if not cls:
            return abort(404)

        if cls.owner.id != g.user.id:
            return abort(403)

        task = (
            Task
            .query
            .filter_by(class_id=cls.id, id=request.get_json().get("task_id"))
            .first()
        )

        if not task:
            return abort(400)

        self.app.db.session.delete(task)
        self.app.db.session.commit()

        return "OK", 200

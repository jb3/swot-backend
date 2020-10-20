"""Provide information on task completions of a class to a teacher."""

from flask import Response, abort, g, render_template, request, jsonify

from backend.models import (
    Class, UserType, ClassMembership,
    Task, TaskCompletion, TaskCompletionStatus
)
from backend.route import Route
from backend.utils import authenticated


class ClassCompletion(Route):
    """A route for displaying completions of students."""

    name = "completions"
    path = "/<int:class_id>/completions"

    @authenticated(user_type=UserType.TEACHER)
    def get(self, class_id: int) -> Response:  # skipcq: PYL-R0201
        """Display a portal page to the user for task completions."""
        cls = Class.query.filter_by(id=class_id).first()

        if not cls:
            return abort(404)

        if cls.owner.id != g.user.id:
            return abort(403)

        render_tasks = set()

        for task in cls.tasks:
            for completion in task.completions:
                if completion.status is TaskCompletionStatus.AWAITING_REVIEW:
                    render_tasks.add(task.id)

        return render_template(
            "teacher/class/completions.html",
            cls=cls,
            render_tasks=render_tasks
        )

    @authenticated(user_type=UserType.TEACHER)
    def post(self, class_id: int) -> Response:
        """Update a task completion in the task."""
        cls = Class.query.filter_by(id=class_id).first()

        if not cls:
            return abort(404)

        if cls.owner.id != g.user.id:
            return abort(403)

        data = request.get_json()

        if data["status"] not in ["complete", "uncomplete"]:
            return abort(403)

        task = Task.query.filter_by(id=data["taskID"], class_id=class_id).first()

        if not task:
            return abort(405)

        if ClassMembership.query.filter_by(
            class_id=class_id,
            user_id=data["userID"]
        ).first():
            if task_completion := TaskCompletion.query.filter_by(
                task_id=data["taskID"],
                user_id=data["userID"]
            ).first():
                task_completion.status = TaskCompletionStatus(data["status"])
                self.app.db.session.commit()
                return "OK"
            else:
                return abort(405)
        else:
            return abort(405)

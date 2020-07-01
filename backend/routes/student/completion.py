"""A set of routes to allow students to mark tasks as complete."""

from flask import abort, g, Response, request

from backend.models import Task, TaskCompletionStatus, TaskCompletion, UserType
from backend.route import Route
from backend.utils import authenticated


class StudentTaskCompletion(Route):
    """A route to allow students to alter the type of a task."""

    name = "completions"
    path = "/task/<int:task_id>/status"

    @authenticated(user_type=UserType.STUDENT)
    def post(self, task_id: int) -> Response:
        """Alter the status of a task."""
        form = request.get_json()

        task = Task.query.filter_by(id=task_id).first()

        if not task:
            abort(404)

        if new_status := form.get("status"):
            existing = TaskCompletion.query.filter_by(
                user_id=g.user.id,
                task_id=task_id
            ).first()

            if existing:
                if existing.status is TaskCompletionStatus.AWAITING_REVIEW:
                    abort(403)

            if g.user.id not in [u.user.id for u in task.cls.members]:
                abort(401)

            if not existing:
                if new_status == "COMPLETE":
                    status = TaskCompletion(
                        task_id=task_id,
                        user_id=g.user.id,
                        status=TaskCompletionStatus.AWAITING_REVIEW
                    )

                    self.app.db.session.add(status)
                    self.app.db.session.commit()
                elif new_status == "UNCOMPLETE":
                    status = TaskCompletion(
                        task_id=task_id,
                        user_id=g.user.id,
                        status=TaskCompletionStatus.UNCOMPLETE
                    )
            else:
                if new_status == "COMPLETE":
                    existing.status = TaskCompletionStatus.AWAITING_REVIEW
                elif new_status == "UNCOMPLETE":
                    existing.status = TaskCompletionStatus.UNCOMPLETE

                self.app.db.session.commit()

        return "ok"

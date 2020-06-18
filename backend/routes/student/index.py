"""A portal for allowing students to see their classes."""

from datetime import datetime
from itertools import groupby

from flask import g, Response, render_template

from backend.models import UserType
from backend.route import Route
from backend.utils import authenticated

WEEK_DAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

SUFFIXES = {
    1: "st",
    2: "nd",
    3: "rd",
    range(4, 21): "th",
    21: "st",
    22: "nd",
    23: "rd",
    range(24, 31): "th",
    31: "st",
}

MONTHS = [
    None,
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


class StudentPortal(Route):
    """A route for displaying student classes."""

    name = "index"
    path = "/"

    @staticmethod
    def format_date(date: datetime) -> str:
        weekday = WEEK_DAYS[date.weekday()]

        suffix = ""

        for day_or_range, suf in SUFFIXES.items():
            if isinstance(day_or_range, int):
                if date.day == day_or_range:
                    suffix = suf
            else:
                if date.day in day_or_range:
                    suffix = suf

        return f"{weekday}, {date.day}{suffix} {MONTHS[date.month]}, {date.year}"

    @authenticated(user_type=UserType.STUDENT)
    def get(self) -> Response:  # skipcq: PYL-R0201
        """Display a portal page to the user."""
        classes = g.user.classes

        tasks = []

        for cm in classes:
            tasks.extend(cm.cls.tasks)

        tasks_by_date = groupby(tasks, lambda task: self.format_date(task.due_at))

        return render_template(
            "student/index.html", formatter=self.format_date, tasks=tasks_by_date
        )

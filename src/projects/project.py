from datetime import datetime
from typing import Optional
from observers import *


class TaggingMixin:
    def __init__(self, tags: Optional[list] = None):
        super().__init__()
        self._tags = tags if tags else []


    @property
    def tags(self):
        return self._tags


    def add_tag(self, tag: str):
        if tag not in self._tags:
            self._tags.append(tag)


    def remove_tag(self, tag: str):
        if tag in self._tags:
            self._tags.remove(tag)


class TimestampMixin:
    def __init__(self):
        super().__init__()
        self._created_at = datetime.now()
        self._updated_at = datetime.now()


    @property
    def created_at(self):
        return self._created_at


    @property
    def updated_at(self):
        return self._updated_at


    @updated_at.setter
    def updated_at(self, value = datetime.now()):
        self._updated_at = value


class Project(TimestampMixin, TaggingMixin, Observable):
    def __init__(
            self,
            project_id: int,
            user_id: int,
            title: str,
            description: str,
            goal_amount: float,
            current_amount: float = 0.0,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None,
            category_id: Optional[int] = None,
            status: str = "active",
            project_image: Optional[bytes] = None,
            milestones_id: Optional[int] = None,
    ) -> None:
        super().__init__()

        self._project_id = project_id
        self._user_id = user_id
        self._title = title
        self._description = description
        self._goal_amount = goal_amount
        self._current_amount = current_amount
        self._start_date = start_date if start_date else datetime.now()
        self._end_date = end_date
        self._category_id = category_id
        self._status = status
        self._project_image = project_image
        self._milestones_id = milestones_id


    @property
    def title(self):
        return self._title

    @property
    def current_amount(self) -> float:
        return self._current_amount

    @property
    def description(self):
        return self._description

    def adjust_amount(self, amount: float) -> None:
        self._current_amount += amount
        self.updated_at = datetime.now()
        self.notify_observers(f"Project '{self._title}' amount updated by {amount}. New total: {self._current_amount}")


    def add_milestone(self, milestone: str) -> None:
        self._milestones_id = milestone
        self.updated_at = datetime.now()
        self.notify_observers(f"Milestone '{milestone}' added to project '{self._title}'.")


    def update_status(self, new_status: str) -> None:
        self._status = new_status
        self.updated_at = datetime.now()
        self.notify_observers(f"Project '{self._title}' status updated to '{new_status}'.")


    def is_active(self) -> bool:
        now = datetime.now()
        return self._start_date <= now and (self._end_date is None or now <= self._end_date)


    def __str__(self) -> str:
        return (f"Project({self._title}, Status: {self._status}, "
                f"Created at: {self.created_at}, Updated at: {self.updated_at}, "
                f"Goal: {self._goal_amount}, Current: {self._current_amount})")
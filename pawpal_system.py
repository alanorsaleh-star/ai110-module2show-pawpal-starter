"""PawPal+ core domain model.

This module contains the core classes used to represent the
pet owner, pet, care tasks, and the scheduler that generates
a daily plan.

The implementations here are intentionally minimal skeletons.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, time, timedelta
from typing import Any, Dict, List, Optional


@dataclass
class PetOwner:
    """Represents the pet owner and their scheduling constraints."""

    name: str
    email: Optional[str] = None
    daily_available_minutes: Optional[int] = None
    preferences: Dict[str, Any] = field(default_factory=dict)
    time_zone: Optional[str] = None

    def update_preferences(self, **prefs: Any) -> None:
        """Update owner preferences."""
        self.preferences.update(prefs)

    def set_availability(self, start_time: time, end_time: time) -> None:
        """Set the owner's available time window for care tasks."""
        # TODO: Convert to internal representation (e.g. minutes available)
        pass

    def get_available_windows(self) -> List[tuple[time, time]]:
        """Return a list of available time windows (start/end pairs)."""
        return []

    def is_available_for(self, task: "Task") -> bool:
        """Return True if task can be scheduled given owner constraints."""
        return True


@dataclass
class Pet:
    """Represents the pet being cared for."""

    name: str
    type: str
    age: Optional[int] = None
    needs: List[str] = field(default_factory=list)
    health_notes: Optional[str] = None

    def add_need(self, category: str, details: Optional[str] = None) -> None:
        """Add a new care need/category for the pet."""
        self.needs.append(category)

    def describe(self) -> str:
        """Return a short description of the pet."""
        return f"{self.name} ({self.type})"

    def needs_attention(self) -> List[str]:
        """Return list of needs that currently require attention."""
        return []


@dataclass
class Task:
    """Represents a care task that can be scheduled."""

    title: str
    duration_minutes: int
    priority: str
    category: str
    preferred_time: Optional[tuple[time, time]] = None
    notes: Optional[str] = None
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def reschedule(self, new_start: datetime) -> None:
        """Reschedule the task to a new start time."""
        # TODO: Store the scheduled time if tracking it
        pass

    def is_due(self, now: Optional[datetime] = None) -> bool:
        """Determine whether the task should be scheduled now."""
        return False

    def to_display_string(self) -> str:
        """Return a human-friendly task description."""
        return f"{self.title} ({self.duration_minutes}m, {self.priority})"


@dataclass
class Schedule:
    """Represents a daily schedule/plan."""

    date: datetime
    tasks: List[Task] = field(default_factory=list)
    explanation: Optional[str] = None

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        self.tasks = [t for t in self.tasks if t is not task]

    def get_conflicts(self) -> List[tuple[Task, Task]]:
        """Return pairs of tasks that conflict (overlap) in time."""
        return []

    def summarize(self) -> str:
        """Return a human-readable summary of the schedule."""
        return "\n".join([t.to_display_string() for t in self.tasks])


class Scheduler:
    """Schedules tasks into a daily plan based on constraints."""

    def __init__(
        self,
        owner: PetOwner,
        pet: Pet,
        tasks: Optional[List[Task]] = None,
        day_start: Optional[time] = None,
        day_end: Optional[time] = None,
    ):
        self.owner = owner
        self.pet = pet
        self.tasks = tasks or []
        self.day_start = day_start
        self.day_end = day_end

    def generate_plan(self, date: datetime) -> Schedule:
        """Generate a schedule for the given date."""
        return Schedule(date=date)

    def rank_tasks(self) -> List[Task]:
        """Return tasks ordered by priority and other signals."""
        return sorted(self.tasks, key=lambda t: t.priority)

    def fit_tasks_into_window(
        self, tasks: List[Task], available_windows: List[tuple[time, time]]
    ) -> Schedule:
        """Attempt to place tasks into available time windows."""
        return Schedule(date=datetime.now())

    def explain_plan(self, schedule: Schedule) -> str:
        """Return a short explanation of why tasks were scheduled the way they were."""
        return schedule.explanation or ""

    def handle_edge_cases(self) -> None:
        """Handle situations like too many tasks for available time."""
        pass

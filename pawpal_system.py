"""PawPal+ core domain model.

This module contains the core classes used to represent the
pet owner, pet, care tasks, and the scheduler that generates
a daily plan.

The implementations here are intentionally minimal skeletons.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
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
    tasks: List["Task"] = field(default_factory=list)

    @property
    def task_count(self) -> int:
        """Return how many tasks are assigned to this pet."""
        return len(self.tasks)

    def add_task(self, task: "Task") -> None:
        """Assign a task to this pet."""
        self.tasks.append(task)

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
    scheduled_time: Optional[str] = None
    duration_minutes: int = 0
    priority: str = "medium"
    category: str = "general"
    preferred_time: Optional[tuple[time, time]] = None
    notes: Optional[str] = None
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None
    due_date: Optional[date] = None
    completed: bool = False

    def mark_complete(self) -> Optional["Task"]:
        """Mark the task as completed.

        If the task is recurring (daily/weekly), return a new Task instance
        representing the next occurrence.
        """
        self.completed = True

        if not self.is_recurring or not self.recurrence_pattern:
            return None

        # Normalize recurrence keyword to lower-case for easier matching.
        pattern = self.recurrence_pattern.strip().lower()
        if pattern not in {"daily", "weekly"}:
            return None

        # Calculate the next due date using timedelta.
        # For daily recurrence, add 1 day. For weekly, add 7 days.
        base_date = self.due_date or date.today()
        delta = timedelta(days=1 if pattern == "daily" else 7)
        next_due = base_date + delta

        return Task(
            title=self.title,
            scheduled_time=self.scheduled_time,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            category=self.category,
            preferred_time=self.preferred_time,
            notes=self.notes,
            is_recurring=self.is_recurring,
            recurrence_pattern=self.recurrence_pattern,
            due_date=next_due,
        )

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

    @staticmethod
    def _parse_time(value: Optional[str]) -> Optional[time]:
        """Parse a time string (HH:MM) into a `time` object."""
        if not value:
            return None
        try:
            return datetime.strptime(value, "%H:%M").time()
        except ValueError:
            return None

    @staticmethod
    def _task_start_time(task: Task) -> Optional[time]:
        """Determine the earliest known start time for a task."""
        # Prefer an explicitly scheduled time
        if task.scheduled_time:
            parsed = Scheduler._parse_time(task.scheduled_time)
            if parsed:
                return parsed

        # Fall back to the preferred time window, if available
        if task.preferred_time:
            return task.preferred_time[0]

        return None

    def sort_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Sort tasks by start time and filter out tasks without any time data."""
        tasks = tasks if tasks is not None else self.tasks

        def sort_key(task: Task) -> time:
            start = self._task_start_time(task)
            # Put tasks without a time at the end
            return start or time.max

        # Only keep tasks that have at least some time information.
        filtered = [t for t in tasks if self._task_start_time(t) is not None]
        return sorted(filtered, key=sort_key)

    def generate_plan(self, date: datetime) -> Schedule:
        """Generate a schedule for the given date."""
        schedule = Schedule(date=date)
        for task in self.sort_by_time():
            schedule.add_task(task)
        return schedule

    def rank_tasks(self) -> List[Task]:
        """Return tasks ordered by priority and other signals."""
        return sorted(self.tasks, key=lambda t: t.priority)

    def fit_tasks_into_window(
        self, tasks: List[Task], available_windows: List[tuple[time, time]]
    ) -> Schedule:
        """Attempt to place tasks into available time windows."""
        return Schedule(date=datetime.now())

    def _get_task_time_range(self, task: Task) -> Optional[tuple[time, time]]:
        """Extract the effective start/end time (range) for a task.

        Returns None if there is no time information available.
        """
        # Prefer exact scheduled time (a point in time) but treat it as a range.
        if task.scheduled_time:
            start = self._parse_time(task.scheduled_time)
            if start:
                end = (datetime.combine(date.today(), start) + timedelta(minutes=task.duration_minutes)).time()
                return start, end

        # Fallback to preferred time window
        return task.preferred_time

    def get_conflicts(self, schedule: Schedule) -> List[str]:
        """Return a list of warnings for tasks that conflict in time."""
        warnings: List[str] = []

        ranges: List[tuple[Task, tuple[time, time]]] = []
        for task in schedule.tasks:
            time_range = self._get_task_time_range(task)
            if time_range:
                ranges.append((task, time_range))

        # Compare each pair of tasks for overlap.
        for i in range(len(ranges)):
            task1, (start1, end1) = ranges[i]
            for j in range(i + 1, len(ranges)):
                task2, (start2, end2) = ranges[j]
                # Overlap if intervals intersect
                if start1 < end2 and start2 < end1:
                    warnings.append(
                        f"Conflict: '{task1.title}' and '{task2.title}' overlap in time."
                    )

        return warnings

    def handle_edge_cases(self) -> None:
        """Handle situations like too many tasks for available time."""
        pass

from datetime import date, datetime

from pawpal_system import PetOwner, Pet, Schedule, Scheduler, Task


def test_pet_task_count():
    pet = Pet("Buddy", "Dog")

    # Verify initial task count
    assert pet.task_count == 0

    # Add a task and verify count increased
    task = Task("Feed", "08:00")
    pet.add_task(task)
    assert pet.task_count == 1

    # Add another task and verify count increased again
    task2 = Task("Walk", "18:00")
    pet.add_task(task2)
    assert pet.task_count == 2


def test_sort_tasks_by_time():
    owner = PetOwner(name="Test", email="test@example.com")
    pet = Pet(name="Buddy", type="Dog")

    t1 = Task(title="Task 1", scheduled_time="09:00")
    t2 = Task(title="Task 2", scheduled_time="08:00")
    t3 = Task(title="Task 3")  # no time should be filtered out

    scheduler = Scheduler(owner=owner, pet=pet, tasks=[t1, t2, t3])
    sorted_tasks = scheduler.sort_by_time()

    assert [t.title for t in sorted_tasks] == ["Task 2", "Task 1"]


def test_daily_recurrence_creates_next_task():
    task = Task(
        title="Daily check",
        scheduled_time="10:00",
        duration_minutes=10,
        is_recurring=True,
        recurrence_pattern="daily",
        due_date=date(2026, 3, 16),
    )

    next_task = task.mark_complete()

    assert task.completed
    assert next_task is not None
    assert next_task.due_date == date(2026, 3, 17)


def test_conflict_detection_finds_overlaps():
    owner = PetOwner(name="Test", email="test@example.com")
    pet = Pet(name="Buddy", type="Dog")

    t1 = Task(title="Task 1", scheduled_time="08:00", duration_minutes=30)
    t2 = Task(title="Task 2", scheduled_time="08:00", duration_minutes=15)

    schedule = Schedule(date=datetime.now())
    schedule.add_task(t1)
    schedule.add_task(t2)

    scheduler = Scheduler(owner=owner, pet=pet, tasks=[t1, t2])
    conflicts = scheduler.get_conflicts(schedule)

    assert len(conflicts) == 1
    assert "overlap" in conflicts[0].lower()

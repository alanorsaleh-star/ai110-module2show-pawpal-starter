"""Quick demo script for PawPal+ scheduling."""

from datetime import datetime, time

from pawpal_system import PetOwner, Pet, Schedule, Scheduler, Task


def format_task(task: Task) -> str:
    preferred = "" if not task.preferred_time else f" (preferred: {task.preferred_time[0].strftime('%H:%M')}–{task.preferred_time[1].strftime('%H:%M')})"
    return f"- {task.to_display_string()}{preferred}"


def main() -> None:
    owner = PetOwner(name="Alex", email="alex@example.com", daily_available_minutes=180)

    pet1 = Pet(name="Milo", type="Dog", age=4)
    pet2 = Pet(name="Whiskers", type="Cat", age=2)

    task1 = Task(
        title="Morning walk",
        duration_minutes=30,
        priority="high",
        category="walk",
        preferred_time=(time(8, 0), time(9, 0)),
        notes="Use the park route",
    )

    task2 = Task(
        title="Feed breakfast",
        duration_minutes=10,
        priority="high",
        category="feeding",
        preferred_time=(time(8, 30), time(9, 0)),
        notes="Dry kibble + wet food",
    )

    task3 = Task(
        title="Give medication",
        duration_minutes=5,
        priority="medium",
        category="meds",
        preferred_time=(time(12, 0), time(12, 15)),
        notes="Give pill with a treat",
    )

    # Create a scheduler for pet1 (demonstrates conflict detection)
    scheduler = Scheduler(owner=owner, pet=pet1, tasks=[task1, task2, task3])
    schedule = scheduler.generate_plan(date=datetime.now())

    # Detect conflicts and warn if found.
    conflicts = scheduler.get_conflicts(schedule)

    print("Today's Schedule")
    print("----------------")
    for t in schedule.tasks:
        print(format_task(t))

    if conflicts:
        print("\nWarnings:")
        for w in conflicts:
            print(w)


if __name__ == "__main__":
    main()

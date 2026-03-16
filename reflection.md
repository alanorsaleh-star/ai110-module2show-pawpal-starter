# PawPal+ Project Reflection

# 3 Core Actions
1. Enter owner and pet info
2. Add/edit tasks
3. Generate and display a daily plan

Main Objects brainstorming:

1. PetOwner/Owner
attributes: 
- name
- email
- daily_available_time
- preference
- time_zone

Methods:
- update_preferences
- set_availability(start_time, end_time)
- get_available_windows()
- is_available_for(task)

2. Pet
attributes:
- name
- type (dog/cat/etc.)
- age
- needs (list of care - categories)
- health_notes (optional)

Methods:
- add_need(category, details)
- describe() / summary()
- needs_attention() (returns list of urgent or overdue needs)

3. Task/CareTask
Attributes:
- title
- duration (minutes)
- priority (numeric or enum: high/medium/low)
- category (walk/feeding/meds/enrichment/etc.)
- preferred_time (optional window or time-of-day)
- notes / instructions
- is_recurring / - recurrence_pattern (optional)
- completed (boolean) or status

Methods:
- mark_complete()
- reschedule(new_time)
- is_due(now) / needs_scheduling()
- to_display_string() (for UI output)


4. Scheduler
Attributes:
- owner / owner constraints
- pet (or pet set)
- tasks (task pool to schedule from)
- day_length / time window (e.g., 8am–8pm)

Methods:
- generate_plan(date) (returns a Schedule)
- rank_tasks() (sort tasks by priority + constraints)
- fit_tasks_into_window(tasks, available_windows)
- explain_plan(schedule) (reasoning logic)
- handle_edge_cases() (e.g., too many tasks for available time)

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

- PetOwner
Role: Holds the owner’s profile and scheduling constraints.
Responsibilities: Store availability/preferences, answer questions like “is this task okay for the owner’s schedule?”

- Pet
Role: Represents the animal being cared for.
Responsibilities: Track pet identity + needs (e.g., “needs feeding”, “needs meds”), and expose a summary or “needs attention” list.

- Task
Role: Models a single care activity (walk, feed, meds, etc.).
Responsibilities: Store duration/priority/category/preferred time, allow marking complete/rescheduling, and provide a human-friendly repr.

- Scheduler
Role: The “brain” that turns tasks + constraints into a daily plan.
Responsibilities: Rank tasks, fit them into available time windows, generate a Schedule, and explain why it chose that plan.

- Schedule (supporting class)
Role: Holds the output plan for a specific date.
Responsibilities: Maintain ordered tasks, detect conflicts, and provide a summary/explanation.


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
Yes, one class was added (a supporting class).
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- One tradeoff the scheduler makes is that it only detects conflicts when two tasks overlap exactly in time ranges (based on scheduled time + duration or preferred time window). It does not attempt to resolve conflicts, merge tasks, or reason about partial overlaps beyond a simple time intersection check.
- This is reasonable for the project scope because it keeps the logic lightweight and predictable, and it provides a clear warning to the user without introducing complex scheduling heuristics that are harder to test and explain.

---

## 3. AI Collaboration

**a. How you used AI**

- I used VS Code Copilot (and the Copilot chat agent) for **design brainstorming**, **refactoring**, and **writing tests**.
- The most helpful Copilot features were:
  - **Inline code completion** to scaffold class methods and small helper functions quickly.
  - **Copilot Chat** for generating test ideas, refactoring suggestions, and getting quick explanations of algorithms.
  - The **Generate tests** smart action to bootstrap pytest cases.

**b. Judgment and verification**

- One example where I rejected an AI suggestion: Copilot suggested implementing conflict detection by comparing only exact `scheduled_time` strings, which would miss overlapping time windows. I modified it to compare actual time intervals for better real-world behavior and clearer conflict warnings.
- I verified AI suggestions by running the existing test suite and writing new tests that asserted the desired behavior (e.g., overlapping tasks produce a warning).

**c. Chat session separation**

- Splitting work into separate Copilot chat sessions helped keep each phase focused and prevented earlier discussions from polluting later ones.
- For example, the “design” session focused on class structure, while the “testing” session focused purely on edge cases and test coverage.

**d. Being the lead architect**

- Working with AI means you still need to **decide what’s important**, choose tradeoffs, and keep the system coherent.
- I treated Copilot as a helpful partner that can prototype ideas quickly, but I always reviewed suggestions for correctness and maintainability before accepting them.

---

## 4. Testing and Verification

**a. What you tested**

- I tested that values are tracked correctly on the domain layer (a `Pet` knows how many tasks it has).
- I verified that the scheduler correctly sorts tasks by time and filters out tasks that have no time information.
- I tested recurrence logic so that marking a daily task complete produces a new task due the next day.
- I tested conflict detection to ensure overlapping tasks generate a warning.

These tests are important because they validate the core behaviors that make the scheduler useful: ordering tasks, repeating them on a cadence, and alerting the user when the plan conflicts.

**b. Confidence**

- I'm reasonably confident the core scheduler logic works for the documented behaviors. The tests cover the main happy paths and a few common edge cases.
- If I had more time, I would write additional tests for:
  - multiple pets and shared resources (tasks that conflict across different pets)
  - tasks with missing or invalid time strings
  - recurrence patterns beyond daily/weekly (e.g., every other day)
  - tasks that span midnight or cross multiple days

---

## 5. Reflection

**a. What went well**

- I’m most satisfied with getting a working backend scheduler with tests, and then plugging that into the UI quickly so it feels like a real app.
- The combination of small, focused unit tests and a simple Streamlit UI made it easy to iterate without breaking existing behavior.

**b. What you would improve**

- I would improve the scheduler to support multi-pet planning (so the owner can see a full day across all pets) and more flexible conflict resolution (e.g., suggest alternative times).
- I would also make the recurrence system more robust, supporting more patterns and letting the user edit the next occurrence.

**c. Key takeaway**

- Building with AI as a partner is most effective when you stay in control of the architecture: decide the responsibilities, verify suggestions with tests, and keep the system simple enough to reason about.

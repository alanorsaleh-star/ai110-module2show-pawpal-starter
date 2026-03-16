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

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

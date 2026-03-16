import streamlit as st
from datetime import datetime

from pawpal_system import PetOwner, Pet, Task, Scheduler, Schedule


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# --- Session state setup ---
if "owner" not in st.session_state:
    st.session_state.owner = PetOwner(name="Jordan")

if "pets" not in st.session_state:
    st.session_state.pets = []

if "tasks" not in st.session_state:
    st.session_state.tasks = []


def format_task(task: Task) -> str:
    return f"{task.title} ({task.duration_minutes}m, {task.priority})"


# --- Owner & pets ---
st.subheader("Owner and Pets")
owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
st.session_state.owner.name = owner_name

pet_name = st.text_input("New pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"], index=0)

if st.button("Add pet"):
    new_pet = Pet(name=pet_name, type=species)
    st.session_state.pets.append(new_pet)

if st.session_state.pets:
    st.write("Current pets:")
    pets_table = [
        {"name": p.name, "type": p.type, "task_count": p.task_count}
        for p in st.session_state.pets
    ]
    st.table(pets_table)
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Tasks ---
st.subheader("Tasks")
st.caption("Add tasks and assign them to a pet. These feed into the scheduler.")

selected_pet_index = 0
if st.session_state.pets:
    pet_names = [p.name for p in st.session_state.pets]
    selected_pet_index = st.selectbox("Assign task to", range(len(pet_names)), format_func=lambda i: pet_names[i])

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    if not st.session_state.pets:
        st.warning("Add a pet first before assigning tasks.")
    else:
        task = Task(title=task_title, duration_minutes=int(duration), priority=priority)
        pet = st.session_state.pets[selected_pet_index]
        pet.add_task(task)
        st.session_state.tasks.append(task)

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "task": format_task(t),
                "assigned_to": next((p.name for p in st.session_state.pets if t in p.tasks), "-"),
            }
            for t in st.session_state.tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- Scheduling ---
st.subheader("Build Schedule")
st.caption("Click to generate a schedule using your scheduler logic.")

if st.button("Generate schedule"):
    if not st.session_state.pets:
        st.warning("Add at least one pet before generating a schedule.")
    else:
        owner = st.session_state.owner
        pet = st.session_state.pets[0]
        scheduler = Scheduler(owner=owner, pet=pet, tasks=pet.tasks)
        schedule = scheduler.generate_plan(date=datetime.now())

        # Fallback: if generate_plan doesn't yet populate tasks, use the pet tasks.
        if not schedule.tasks:
            for t in pet.tasks:
                schedule.add_task(t)

        st.markdown("### Today's Schedule")
        st.markdown(schedule.summarize())

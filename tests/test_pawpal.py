from pawpal_system import Task, Pet

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
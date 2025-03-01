import json
import os
import uuid
from datetime import datetime


TASK_FILE = 'tasks.json'


# data model for a task

class Task:
    def __init__(self, title, description):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.completed = False
        self.created_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            'id': self.id,
            'due_date': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at
        }


    @staticmethod
    def from_dict(data):
        task = Task(data['title'], data['description'])
        task.id = data['id']
        task.completed = data['completed']
        task.created_at = data['created_at']
        return task


# fn to handle file storage
def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []
    with open(TASK_FILE, 'r') as f:
        tasks = json.load(f)
        return [Task.from_dict(data) for data in tasks]

def save_tasks(tasks):
    with open(TASK_FILE, 'w') as f:
        json.dump([task.to_dict() for task in tasks], f, indent=4)


#ui functions

def display_menu():
    print("Task Manager")
    print("1. List tasks")
    print("2. Add task")
    print("3. Mark task as completed")
    print("4. Remove task")
    print("5. Quit")

def view_tasks(tasks):
    if not tasks:
        print("No tasks")
        return
    print("Tasks:")
    for idx, task in enumerate(tasks, start=1):
        status = '✓' if task.completed else '✗'
        print(f"{idx}. [{status}] {task.title} - {task.description}")

def add_task(tasks):
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    tasks.append(Task(title, description))
    save_tasks(tasks)
    print("Task added")


def mark_task(tasks):
    view_tasks(tasks)
    task_idx = int(input("Enter task number: ")) - 1
    tasks[task_idx].completed = True
    save_tasks(tasks)
    print("Task marked as completed")

def remove_task(tasks):
    view_tasks(tasks)
    if not tasks:
        return
    try:
        task_idx = int(input("Enter task number: ")) - 1
        tasks.pop(task_idx)
        save_tasks(tasks)
        print("Task removed")
    except ValueError:
        print("Invalid input")


def quit_ui():
    print("Goodbye!")
    exit(0)

def  main():
    tasks = load_tasks()
    while True:
        display_menu()
        choice = input("Enter choice: ")
        if choice == '1':
            view_tasks(tasks)
        elif choice == '2':
            add_task(tasks)
        elif choice == '3':
            mark_task(tasks)
        elif choice == '4':
            remove_task(tasks)
        elif choice == '5':
            quit_ui()
            break
        else:
            print("Invalid input")



if __name__ == '__main__':
    main()
import json
import csv
from datetime import datetime

tasks = []

# ----------------------------
# Helper Functions
# ----------------------------

def show_menu():
    print("\n===== TASK MANAGER =====")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Export to JSON")
    print("6. Export to CSV")
    print("7. Exit")

def add_task():
    title = input("Enter task title: ")
    deadline = input("Enter deadline (YYYY-MM-DD): ")
    priority = input("Enter priority (High/Medium/Low): ")

    task = {
        "title": title,
        "deadline": deadline,
        "priority": priority,
        "completed": False
    }

    tasks.append(task)
    print("✅ Task added successfully!")

def view_tasks():
    if not tasks:
        print("No tasks available.")
        return

    print("\n--- Task List ---")
    for i, task in enumerate(tasks):
        status = "✔ Done" if task["completed"] else "❌ Pending"
        print(f"{i+1}. {task['title']} | {task['deadline']} | {task['priority']} | {status}")

def complete_task():
    view_tasks()
    try:
        index = int(input("Enter task number to mark complete: ")) - 1
        tasks[index]["completed"] = True
        print("✅ Task marked as completed!")
    except:
        print("❌ Invalid input.")

def delete_task():
    view_tasks()
    try:
        index = int(input("Enter task number to delete: ")) - 1
        tasks.pop(index)
        print("🗑 Task deleted!")
    except:
        print("❌ Invalid input.")

def export_json():
    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=4)
    print("📁 Exported to tasks.json")

def export_csv():
    with open("tasks.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Deadline", "Priority", "Completed"])
        for task in tasks:
            writer.writerow([
                task["title"],
                task["deadline"],
                task["priority"],
                task["completed"]
            ])
    print("📁 Exported to tasks.csv")

# ----------------------------
# Main Program Loop
# ----------------------------

while True:
    show_menu()
    choice = input("Choose an option: ")

    if choice == "1":
        add_task()
    elif choice == "2":
        view_tasks()
    elif choice == "3":
        complete_task()
    elif choice == "4":
        delete_task()
    elif choice == "5":
        export_json()
    elif choice == "6":
        export_csv()
    elif choice == "7":
        print("👋 Goodbye!")
        break
    else:
        print("❌ Invalid choice. Try again.")
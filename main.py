# read from csv
"""

from core.data_loader import load_employees, load_tasks

employees = load_employees("data/employees.csv")
tasks = load_tasks("data/tasks.csv")

print("Employees:")
for e in employees:
    print(e)

print("\nTasks:")
for t in tasks:
    print(t)

# csp and scheduler
from core.data_loader import load_employees, load_tasks
from core.backtracking_scheduler import BacktrackingScheduler

employees = load_employees("data/employees.csv")
tasks = load_tasks("data/tasks.csv")

scheduler = BacktrackingScheduler(employees, tasks)

schedule = scheduler.solve()

print("\nGenerated Schedule:\n")

if schedule:
    for task_id, value in schedule.assignments.items():
        emp, start, end = value
        print(f"Task {task_id} -> Employee {emp} : {start}-{end}")
else:
    print("No valid schedule found")
"""
from core.data_loader import load_employees, load_tasks
from core.a_star_scheduler import AStarScheduler

employees = load_employees("data/employees.csv")
tasks = load_tasks("data/tasks.csv")

scheduler = AStarScheduler(employees, tasks)

schedule = scheduler.solve()

print("\nOptimized Schedule:\n")

if schedule:
    for task_id, value in schedule.assignments.items():
        emp, start, end = value
        print(f"Task {task_id} -> Employee {emp} : {start}-{end}")
else:
    print("No schedule found")
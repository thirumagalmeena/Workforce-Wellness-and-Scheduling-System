from core.data_loader import load_employees, load_tasks
from core.a_star_scheduler import AStarScheduler
from realtime.event_handler import employee_unavailable
from realtime.adjustment_search import AdjustmentSearch

# ==================== LOAD DATA ====================
employees = load_employees("data/employees.csv")
tasks = load_tasks("data/tasks.csv")

# ==================== INITIAL SCHEDULE ====================
scheduler = AStarScheduler(employees, tasks)
schedule = scheduler.solve()

print("\nInitial Schedule:\n")
for task_id, value in schedule.assignments.items():
    emp, start, end = value
    print(f"Task {task_id} --> Employee {emp} : {start}-{end}")

# ==================== SIMULATE EVENT ====================
print("\nEvent: Employee 1 unavailable\n")

affected = employee_unavailable(schedule, 1)

adjuster = AdjustmentSearch(employees, tasks)

# NEW: adjust now returns (new_schedule, pending)
new_schedule, pending = adjuster.adjust(schedule, affected, 1)

# ==================== UPDATED SCHEDULE ====================
print("\nUpdated Schedule:\n")
for task_id, value in new_schedule.assignments.items():
    emp, start, end = value
    print(f"Task {task_id} --> Employee {emp} : {start}-{end}")

# ==================== PENDING QUEUE ====================
if pending:
    print("\nPending Queue (yet to be assigned - waiting for new employee):")
    for task_id in pending:
        print(f"  --> Task {task_id}")
else:
    print("\n  (All tasks successfully reassigned - no pending tasks)")

from visualization.gantt_chart import plot_schedule

plot_schedule(schedule, employees, tasks)
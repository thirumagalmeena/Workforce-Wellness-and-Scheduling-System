from core.a_star_scheduler import AStarScheduler
from realtime.event_handler import employee_unavailable
from realtime.adjustment_search import AdjustmentSearch
from core.data_loader import load_employees, load_tasks

class SchedulerService:
    def __init__(self):
        self.employees = load_employees("data/employees.csv")
        self.tasks = load_tasks("data/tasks.csv")
        self.schedule = None
        self.run_scheduler()

    def add_employee(self, emp):
        self.employees.append(emp)

    def add_task(self, task):
        self.tasks.append(task)

    def run_scheduler(self):
        scheduler = AStarScheduler(self.employees, self.tasks)
        self.schedule = scheduler.solve()

    def handle_employee_unavailable(self, employee_id):
        affected = employee_unavailable(self.schedule, employee_id)
        adjuster = AdjustmentSearch(self.employees, self.tasks)
        self.schedule = adjuster.adjust(self.schedule, affected)
        return self.get_schedule()
    
    def get_schedule(self):
        if not self.schedule:
            return {
                "schedule": [],
                "pending": self.tasks,
                "idle": self.employees
            }

        emp_map = {e["id"]: e["name"] for e in self.employees}
        task_map = {t["id"]: t["name"] for t in self.tasks}

        formatted = []

        for task_id, (emp, start, end) in self.schedule.assignments.items():
            formatted.append({
                "task": task_map[task_id],
                "employee": emp_map[emp],
                "start": start,
                "end": end
            })

        assigned_ids = self.schedule.assignments.keys()

        pending = [t for t in self.tasks if t["id"] not in assigned_ids]

        assigned_emps = set(emp for emp, _, _ in self.schedule.assignments.values())
        idle = [e for e in self.employees if e["id"] not in assigned_emps]

        return {
            "schedule": formatted,
            "pending": pending,
            "idle": idle
        }
    
    def reset(self):
        """Reset to default data from CSV files"""
        self.employees = load_employees("data/employees.csv")
        self.tasks = load_tasks("data/tasks.csv")
        self.schedule = None
        self.run_scheduler()
        return self.get_schedule()
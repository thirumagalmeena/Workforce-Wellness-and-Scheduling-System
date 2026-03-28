from core.a_star_scheduler import AStarScheduler
from realtime.event_handler import employee_unavailable
from realtime.adjustment_search import AdjustmentSearch
from core.data_loader import load_employees, load_tasks
from backend.wellness_service import WellnessService


class SchedulerService:
    def __init__(self):
        self.employees = load_employees("data/employees.csv")
        self.tasks = load_tasks("data/tasks.csv")
        self.schedule = None
        self.manual_assignments = {}  # {task_id: {"employee_id": X, "start": Y, "end": Z}}
        self.wellness = WellnessService(self.employees, self.tasks)
        self.run_scheduler()

    def add_employee(self, emp):
        self.employees.append(emp)
        self.wellness.update_employees(self.employees)

    def add_task(self, task):
        self.tasks.append(task)

    def run_scheduler(self):
        scheduler = AStarScheduler(self.employees, self.tasks, manual_assignments=self.manual_assignments)
        new_schedule = scheduler.solve()
        
        # If AI couldn't find a full schedule including manuals, it returns None.
        # But we want to keep what we have if possible, or build a partial.
        # A* as written returns best valid state upon hitting end of tasks.
        if new_schedule:
            self.schedule = new_schedule
            self.wellness.record_schedule(self.schedule)
        else:
            # Fallback if impossible: we keep the old schedule but it means manual override broke constraints heavily.
            pass

    def reassign_task(self, task_id: int, new_employee_id: int):
        task = next((t for t in self.tasks if t["id"] == task_id), None)
        emp = next((e for e in self.employees if e["id"] == new_employee_id), None)
        
        if not task or not emp:
            return self.get_schedule()
            
        # Find earliest available slot for new employee that fits duration
        start_time = emp["available_from"]
        
        # Super simple fallback: just put it at their start time, AStar will enforce it if valid, 
        # or we could find the first actual gap. For simulation, let's just place it at their start time.
        self.manual_assignments[task_id] = {
            "employee_id": new_employee_id,
            "start": start_time,
            "end": start_time + task["duration"]
        }
        
        self.run_scheduler()
        return self.get_schedule()

    def handle_employee_unavailable(self, employee_id):
        affected = employee_unavailable(self.schedule, employee_id)
        adjuster = AdjustmentSearch(self.employees, self.tasks)
        self.schedule, _ = adjuster.adjust(self.schedule, affected, employee_id)
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
            "idle": idle,
            "all_employees": self.employees
        }

    # ── Wellness / Fairness pass-throughs ────────────────────────────────────

    def get_wellness_summary(self):
        return self.wellness.get_wellness_summary()

    def get_recommendations(self):
        return self.wellness.get_recommendations()

    def get_fairness_report(self):
        return self.wellness.get_fairness_report()

    def update_wellness_signals(self, employee_id, fatigue=None, stress=None, satisfaction=None):
        return self.wellness.update_wellness_signals(employee_id, fatigue, stress, satisfaction)

    def reset(self):
        """Reset to default data from CSV files"""
        self.employees = load_employees("data/employees.csv")
        self.tasks = load_tasks("data/tasks.csv")
        self.schedule = None
        self.manual_assignments = {}
        self.wellness.reset(self.employees, self.tasks)
        self.run_scheduler()
        return self.get_schedule()
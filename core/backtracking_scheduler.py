from core.state import ScheduleState
from core.constraints import *

class BacktrackingScheduler:
    def __init__(self, employees, tasks):
        self.employees = employees
        self.tasks = tasks

    def solve(self):
        schedule = ScheduleState()
        success = self.backtrack(0, schedule)

        if success:
            return schedule
        else:
            return None

    def backtrack(self, task_index, schedule):
        if task_index == len(self.tasks):
            return True

        task = self.tasks[task_index]

        for employee in self.employees:

            if not check_skill(employee, task):
                continue

            duration = task["duration"]

            for start in range(employee["available_from"], employee["available_to"]):
                end = start + duration

                if not check_availability(employee, start, end):
                    continue

                if not check_deadline(task, end):
                    continue

                if not check_overlap(employee, schedule, start, end):
                    continue

                if not check_max_hours(employee, schedule, duration):
                    continue

                schedule.add(task["id"], employee["id"], start, end)

                if self.backtrack(task_index + 1, schedule):
                    return True

                schedule.remove(task["id"])

        return False
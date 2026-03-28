import itertools
import heapq
from copy import deepcopy
from typing import Optional
from copy import deepcopy
from core.state import ScheduleState
from core.constraints import *
from core.heuristics import schedule_cost

class AStarScheduler:
    def __init__(self, employees, tasks, manual_assignments=None):
        self.employees = employees
        self.tasks = tasks
        self.manual_assignments = manual_assignments or {}
        self.counter = itertools.count()

    def solve(self):
        open_list = []
        initial_state = ScheduleState()
        heapq.heappush(open_list, (0, 0, next(self.counter), initial_state))

        while open_list:
            f, task_index, _, state = heapq.heappop(open_list)

            if task_index == len(self.tasks):
                return state

            task = self.tasks[task_index]
            
            # ── If this task has a manual override, enforce it ────────────────
            if task["id"] in self.manual_assignments:
                assignment = self.manual_assignments[task["id"]]
                emp_id = assignment["employee_id"]
                # Must find the employee to check availability/overlap
                employee = next((e for e in self.employees if e["id"] == emp_id), None)
                if not employee:
                    continue # Invalid manual assignment

                start = assignment["start"]
                end = assignment["end"]

                # Still strictly enforce overlap and hours, to avoid breaking state
                if not check_overlap(employee, state, start, end):
                    continue
                if not check_max_hours(employee, state, end - start):
                    continue

                new_state = deepcopy(state)
                new_state.add(task["id"], employee["id"], start, end)
                g = len(new_state.assignments)
                h = schedule_cost(new_state, self.employees, self.tasks)
                heapq.heappush(open_list, (g + h, task_index + 1, next(self.counter), new_state))
                continue
            # ──────────────────────────────────────────────────────────────────
            # Build all possible valid assignments for this task
            assigned_any = False
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
                    if not check_overlap(employee, state, start, end):
                        continue
                    if not check_max_hours(employee, state, duration):
                        continue

                    new_state = deepcopy(state)
                    new_state.add(task["id"], employee["id"], start, end)

                    # IMPORTANT: In A*, f = g + h. 
                    # We want to MINIMIZE cost.
                    # g is negative of assignments, so more assignments = lower cost.
                    g = -len(new_state.assignments) * 1000  # heavy weight for assigning tasks
                    h = schedule_cost(new_state, self.employees, self.tasks)
                    f = g + h

                    heapq.heappush(open_list, (f, task_index + 1, next(self.counter), new_state))
                    assigned_any = True

            # ALSO ALWAYS ALLOW SKIPPING THIS TASK
            # This ensures we always find a valid path to the end, even if some tasks are dropped.
            # The penalty for skipping is that it has a higher cost (fewer assignments).
            skip_state = deepcopy(state)
            g_skip = -len(skip_state.assignments) * 1000
            h_skip = schedule_cost(skip_state, self.employees, self.tasks)
            heapq.heappush(open_list, (g_skip + h_skip, task_index + 1, next(self.counter), skip_state))

        return None
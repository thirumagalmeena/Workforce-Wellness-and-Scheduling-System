import heapq
import itertools
from copy import deepcopy
from core.constraints import *
from core.heuristics import schedule_cost

class AdjustmentSearch:
    def __init__(self, employees, tasks, max_depth=3):
        self.employees = employees
        self.tasks = tasks
        self.max_depth = max_depth
        self.counter = itertools.count()

    def adjust(self, schedule, affected_tasks, unavailable_id=None):
        open_list = []
        heapq.heappush(open_list, (0, 0, next(self.counter), schedule))

        best_schedule = schedule
        best_cost = schedule_cost(schedule, self.employees, self.tasks)

        if unavailable_id is not None:
            if any(emp == unavailable_id for emp, _, _ in schedule.assignments.values()):
                best_schedule = None
                best_cost = float("inf")

        while open_list:
            cost, depth, _, state = heapq.heappop(open_list)
            if depth >= self.max_depth:
                continue

            for task_id in affected_tasks:
                task = next(t for t in self.tasks if t["id"] == task_id)
                duration = task["duration"]

                for employee in self.employees:
                    if unavailable_id is not None and employee["id"] == unavailable_id:
                        continue

                    for start in range(employee["available_from"], employee["available_to"]):
                        end = start + duration

                        if not check_skill(employee, task): continue
                        if not check_availability(employee, start, end): continue
                        if not check_deadline(task, end): continue
                        if not check_overlap(employee, state, start, end): continue
                        if not check_max_hours(employee, state, duration): continue

                        new_state = deepcopy(state)
                        new_state.add(task_id, employee["id"], start, end)

                        new_cost = schedule_cost(new_state, self.employees, self.tasks)

                        if best_schedule is None or new_cost < best_cost:
                            best_cost = new_cost
                            best_schedule = new_state

                        heapq.heappush(open_list, (new_cost, depth + 1, next(self.counter), new_state))

        pending = []
        if best_schedule is None and unavailable_id is not None:
            print("  --> Local adjustment couldn't find a slot.")
            print("  --> Moving affected task(s) to Pending Queue...")

            best_schedule = deepcopy(schedule)
            for task_id in affected_tasks:
                if task_id in best_schedule.assignments:
                    del best_schedule.assignments[task_id]
                    pending.append(task_id)

            print(f"Tasks {pending} added to pending queue (yet to be assigned)")

        return best_schedule, pending
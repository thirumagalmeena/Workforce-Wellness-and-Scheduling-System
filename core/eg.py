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
        self.counter = itertools.count()  # unique tie-breaker

    def adjust(self, schedule, affected_tasks):

        open_list = []
        # push initial state with counter
        heapq.heappush(open_list, (0, 0, next(self.counter), schedule))

        best_schedule = schedule
        best_cost = schedule_cost(schedule, self.employees, self.tasks)

        while open_list:

            cost, depth, _, state = heapq.heappop(open_list)

            if depth >= self.max_depth:
                continue

            for task_id in affected_tasks:

                task = next(t for t in self.tasks if t["id"] == task_id)

                for employee in self.employees:

                    duration = task["duration"]

                    for start in range(employee["available_from"], employee["available_to"]):

                        end = start + duration

                        if not check_skill(employee, task):
                            continue

                        if not check_availability(employee, start, end):
                            continue

                        if not check_deadline(task, end):
                            continue

                        if not check_overlap(employee, state, start, end):
                            continue

                        if not check_max_hours(employee, state, duration):
                            continue

                        new_state = deepcopy(state)
                        new_state.add(task_id, employee["id"], start, end)

                        new_cost = schedule_cost(new_state, self.employees, self.tasks)

                        if new_cost < best_cost:
                            best_cost = new_cost
                            best_schedule = new_state

                        # add tie-breaker counter to avoid comparing ScheduleState
                        heapq.heappush(open_list, (new_cost, depth + 1, next(self.counter), new_state))

        return best_schedule
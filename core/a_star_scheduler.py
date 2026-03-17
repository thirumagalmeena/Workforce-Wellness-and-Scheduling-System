import itertools
import heapq
from copy import deepcopy
from core.state import ScheduleState
from core.constraints import *
from core.heuristics import schedule_cost

class AStarScheduler:
    def __init__(self, employees, tasks):
        self.employees = employees
        self.tasks = tasks
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

                    g = len(new_state.assignments)
                    h = schedule_cost(new_state, self.employees, self.tasks)
                    f = g + h

                    heapq.heappush(open_list, (f, task_index + 1, next(self.counter), new_state))
        return None
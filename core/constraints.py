def check_skill(employee, task):
    return task["skill"] in employee["skills"]


def check_availability(employee, start, end):
    return start >= employee["available_from"] and end <= employee["available_to"]


def check_max_hours(employee, schedule, duration):
    hours = 0

    for (_, start, end) in schedule.get_employee_tasks(employee["id"]):
        hours += end - start

    return (hours + duration) <= employee["max_hours"]


def check_overlap(employee, schedule, start, end):
    tasks = schedule.get_employee_tasks(employee["id"])

    for (_, s, e) in tasks:
        if not (end <= s or start >= e):
            return False

    return True


def check_deadline(task, end):
    return end <= task["deadline"]


def check_weekly_hours(employee, duration, weekly_hours_used: dict, max_weekly: float = 40.0) -> bool:
    """
    Returns False if assigning this task would push the employee over their
    max weekly hours. weekly_hours_used is {emp_id: hours_so_far}.
    """
    used = weekly_hours_used.get(employee["id"], 0.0)
    return (used + duration) <= max_weekly


def check_consecutive_shifts(employee, wellness_states: dict, max_consecutive: int = 5) -> bool:
    """
    Returns False if the employee has already hit the consecutive shift limit
    (i.e. they need a mandatory break day).
    wellness_states is {emp_id: wellness_state_dict}.
    """
    ws = wellness_states.get(employee["id"])
    if ws is None:
        return True
    return ws["consecutive_shifts"] < max_consecutive
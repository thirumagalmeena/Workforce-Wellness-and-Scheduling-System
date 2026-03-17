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
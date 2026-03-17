def employee_unavailable(schedule, employee_id):
    affected_tasks = []

    for task_id, (emp, start, end) in schedule.assignments.items():
        if emp == employee_id:
            affected_tasks.append(task_id)

    return affected_tasks
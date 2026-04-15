def workload_imbalance(schedule, employees):
    workload = {e["id"]: 0 for e in employees}
    for (_, (emp, start, end)) in schedule.assignments.items():
        workload[emp] += end - start

    values = list(workload.values())
    if len(values) == 0:
        return 0
    return max(values) - min(values)


def deadline_penalty(schedule, tasks):
    penalty = 0
    for task in tasks:
        if task["id"] in schedule.assignments:
            _, _, end = schedule.assignments[task["id"]]
            if end > task["deadline"]:
                penalty += 50
    return penalty


def priority_penalty(schedule, tasks):
    penalty = 0

    if not tasks:
        return 0
    max_priority = max(task["priority"] for task in tasks)

    for task in tasks:
        if task["id"] in schedule.assignments:
            _, _, end = schedule.assignments[task["id"]]
            if end > task["deadline"]:
                penalty += 20 * (max_priority - task["priority"] + 1)

    return penalty


def schedule_cost(schedule, employees, tasks, fairness_tracker=None):
    cost = 0
    cost += workload_imbalance(schedule, employees)
    cost += deadline_penalty(schedule, tasks)
    cost += priority_penalty(schedule, tasks)

    if fairness_tracker is not None:
        cost += fairness_tracker.fairness_penalty(schedule, tasks)

    return cost
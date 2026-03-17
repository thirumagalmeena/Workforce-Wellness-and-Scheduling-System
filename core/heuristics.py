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
    for task in tasks:
        if task["id"] in schedule.assignments:
            _, _, end = schedule.assignments[task["id"]]
            if end > task["deadline"]:
                penalty += 20 * task["priority"]   # heavy penalty for high-priority delays
    return penalty


def schedule_cost(schedule, employees, tasks):
    cost = 0
    cost += workload_imbalance(schedule, employees)
    cost += deadline_penalty(schedule, tasks)
    cost += priority_penalty(schedule, tasks)
    return cost
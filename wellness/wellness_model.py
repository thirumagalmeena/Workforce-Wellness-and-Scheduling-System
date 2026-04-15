DEFAULT_MAX_CONSECUTIVE_SHIFTS = 5   # flag rest if exceeded
DEFAULT_MAX_WEEKLY_HOURS = 40        # hard policy cap


def make_wellness_state(
    employee_id,
    fatigue: float = 3.0,
    stress: float = 3.0,
    satisfaction: float = 7.0,
    consecutive_shifts: int = 0,
    weekly_hours: float = 0.0,
    high_priority_task_count: int = 0,
):
    return {
        "employee_id": employee_id,
        "fatigue": max(0.0, min(10.0, fatigue)),
        "stress": max(0.0, min(10.0, stress)),
        "satisfaction": max(0.0, min(10.0, satisfaction)),
        "consecutive_shifts": consecutive_shifts,
        "weekly_hours": weekly_hours,
        "high_priority_task_count": high_priority_task_count,
    }


def default_wellness_states(employees):

    states = {}
    for emp in employees:
        states[emp["id"]] = make_wellness_state(emp["id"])
    return states


def update_from_schedule(wellness_states, schedule, tasks):

    task_priority = {t["id"]: t["priority"] for t in tasks}

    for task_id, (emp_id, start, end) in schedule.assignments.items():
        ws = wellness_states.get(emp_id)
        if ws is None:
            continue
        duration = end - start
        ws["weekly_hours"] += duration
        priority = task_priority.get(task_id, 1)
        if priority >= 4:
            ws["high_priority_task_count"] += 1

    # Employees who received at least one assignment get +1 consecutive shift
    assigned_emps = set(emp for emp, _, _ in schedule.assignments.values())
    for emp_id in assigned_emps:
        ws = wellness_states.get(emp_id)
        if ws:
            ws["consecutive_shifts"] += 1
            # Derived heuristics for fatigue / stress
            if ws["weekly_hours"] > 35:
                ws["fatigue"] = min(10.0, ws["fatigue"] + 1.5)
                ws["stress"] = min(10.0, ws["stress"] + 1.0)
            if ws["high_priority_task_count"] >= 3:
                ws["stress"] = min(10.0, ws["stress"] + 1.5)
            # Satisfaction drops when overworked
            if ws["weekly_hours"] > 40:
                ws["satisfaction"] = max(0.0, ws["satisfaction"] - 2.0)

    return wellness_states

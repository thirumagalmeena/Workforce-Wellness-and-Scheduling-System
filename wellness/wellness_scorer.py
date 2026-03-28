"""
Wellness scoring engine.

Score formula (0–100):
  base = 100
  - fatigue  * 4   (max penalty: 40)
  - stress   * 3   (max penalty: 30)
  + satisfaction * 2  (max bonus: 20)
  - consecutive_shift_penalty
  - overwork_penalty

Tags: Excellent (80-100), Good (60-79), Fair (40-59), At Risk (<40)
"""

from wellness.wellness_model import DEFAULT_MAX_CONSECUTIVE_SHIFTS, DEFAULT_MAX_WEEKLY_HOURS


def compute_wellness_score(ws: dict) -> dict:
    """
    Given a wellness state dict, return an enriched dict with:
      - score (0–100 float)
      - tag   (str)
      - breakdown (dict of components)
    """
    fatigue = ws["fatigue"]
    stress = ws["stress"]
    satisfaction = ws["satisfaction"]
    consecutive = ws["consecutive_shifts"]
    weekly_hours = ws["weekly_hours"]

    fatigue_pen = fatigue * 4.0
    stress_pen = stress * 3.0
    satisfaction_bonus = satisfaction * 2.0

    # Consecutive shift penalty: 5 pts deducted per shift beyond the threshold
    consecutive_pen = max(0, consecutive - DEFAULT_MAX_CONSECUTIVE_SHIFTS) * 5.0

    # Overwork penalty: 1 pt per hour beyond max weekly hours
    overwork_pen = max(0, weekly_hours - DEFAULT_MAX_WEEKLY_HOURS) * 1.0

    raw = 100 - fatigue_pen - stress_pen + satisfaction_bonus - consecutive_pen - overwork_pen
    score = max(0.0, min(100.0, raw))

    if score >= 80:
        tag = "Excellent"
        tag_color = "green"
    elif score >= 60:
        tag = "Good"
        tag_color = "blue"
    elif score >= 40:
        tag = "Fair"
        tag_color = "orange"
    else:
        tag = "At Risk"
        tag_color = "red"

    return {
        "employee_id": ws["employee_id"],
        "score": round(score, 1),
        "tag": tag,
        "tag_color": tag_color,
        "breakdown": {
            "fatigue_penalty": round(fatigue_pen, 1),
            "stress_penalty": round(stress_pen, 1),
            "satisfaction_bonus": round(satisfaction_bonus, 1),
            "consecutive_penalty": round(consecutive_pen, 1),
            "overwork_penalty": round(overwork_pen, 1),
        },
        "fatigue": ws["fatigue"],
        "stress": ws["stress"],
        "satisfaction": ws["satisfaction"],
        "consecutive_shifts": ws["consecutive_shifts"],
        "weekly_hours": ws["weekly_hours"],
        "high_priority_task_count": ws["high_priority_task_count"],
    }


def score_all_employees(wellness_states: dict, employees: list) -> list:
    """
    Score every employee and attach their name.
    Returns a list sorted by score ascending (worst first).
    """
    emp_names = {e["id"]: e["name"] for e in employees}
    results = []
    for emp_id, ws in wellness_states.items():
        scored = compute_wellness_score(ws)
        scored["name"] = emp_names.get(emp_id, f"Employee {emp_id}")
        results.append(scored)
    results.sort(key=lambda x: x["score"])
    return results

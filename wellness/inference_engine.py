"""
Rule-Based Inference Engine.

Analyses wellness state and fuzzy outputs to:
  1. Trigger concrete actions: enforce_break, reduce_workload, rotation_needed, flag_rest
  2. Generate personalized text recommendations
  3. Run a non-diagnostic symptom checker (flags when rest may be needed)
"""

from wellness.wellness_model import DEFAULT_MAX_CONSECUTIVE_SHIFTS, DEFAULT_MAX_WEEKLY_HOURS


# ─── Symptom Checker (non-diagnostic) ────────────────────────────────────────

def symptom_check(ws: dict) -> dict:
    """
    Non-diagnostic check: flags observable work-pattern signals.
    Returns a dict of {signal: bool, ...} and a summary message.
    """
    signals = {
        "high_fatigue":           ws["fatigue"] >= 7.0,
        "high_stress":            ws["stress"] >= 7.0,
        "low_satisfaction":       ws["satisfaction"] <= 3.0,
        "overworked":             ws["weekly_hours"] > DEFAULT_MAX_WEEKLY_HOURS,
        "consecutive_limit":      ws["consecutive_shifts"] >= DEFAULT_MAX_CONSECUTIVE_SHIFTS,
        "heavy_priority_load":    ws["high_priority_task_count"] >= 3,
    }
    triggered = [k for k, v in signals.items() if v]
    rest_recommended = len(triggered) >= 2

    return {
        "signals": signals,
        "triggered": triggered,
        "rest_recommended": rest_recommended,
        "message": (
            "⚠️ Multiple wellness signals detected — rest or workload reduction recommended."
            if rest_recommended else
            "✅ No critical wellness signals."
        ),
    }


# ─── Action Triggers ─────────────────────────────────────────────────────────

def derive_actions(ws: dict, fuzzy_out: dict) -> list:
    """
    Derive a list of action strings from wellness state + fuzzy output.
    Actions: "enforce_break", "reduce_workload", "rotation_needed", "flag_rest", "no_action"
    """
    actions = []

    if ws["consecutive_shifts"] >= DEFAULT_MAX_CONSECUTIVE_SHIFTS:
        actions.append("enforce_break")

    if fuzzy_out["workload_reduction"] >= 0.6:
        actions.append("reduce_workload")

    if ws["high_priority_task_count"] >= 3:
        actions.append("rotation_needed")

    symptom = symptom_check(ws)
    if symptom["rest_recommended"]:
        actions.append("flag_rest")

    if not actions:
        actions.append("no_action")

    return list(set(actions))   # deduplicate


# ─── Recommendation Text Generator ───────────────────────────────────────────

_ACTION_TEMPLATES = {
    "enforce_break": (
        "🔴 Mandatory Break Required: {name} has worked {consecutive_shifts} consecutive "
        "shifts (threshold: {max_cons}). Schedule a recovery day before the next assignment."
    ),
    "reduce_workload": (
        "🟠 Reduce Workload: Fuzzy analysis indicates {name}'s workload should be reduced by "
        "~{reduction_pct}%. Assign shorter or lower-complexity tasks next cycle."
    ),
    "rotation_needed": (
        "🔄 Rotation Suggested: {name} has handled {hpt} high-priority tasks. Rotate lighter "
        "tasks to restore balance and prevent burnout."
    ),
    "flag_rest": (
        "⚠️  Rest Flag: {name}'s wellness signals (fatigue={fatigue:.1f}, stress={stress:.1f}, "
        "satisfaction={satisfaction:.1f}) suggest rest may help. Monitor closely."
    ),
    "no_action": (
        "✅ {name} is on track — no wellness interventions needed this cycle."
    ),
}


def generate_recommendations(ws: dict, fuzzy_out: dict, name: str) -> list:
    """
    Return a list of recommendation strings for one employee.
    """
    actions = derive_actions(ws, fuzzy_out)
    recs = []
    for action in actions:
        template = _ACTION_TEMPLATES.get(action, "")
        if template:
            recs.append(template.format(
                name=name,
                consecutive_shifts=ws["consecutive_shifts"],
                max_cons=DEFAULT_MAX_CONSECUTIVE_SHIFTS,
                reduction_pct=round(fuzzy_out["workload_reduction"] * 100),
                hpt=ws["high_priority_task_count"],
                fatigue=ws["fatigue"],
                stress=ws["stress"],
                satisfaction=ws["satisfaction"],
            ))
    return recs


# ─── Batch Inference ─────────────────────────────────────────────────────────

def run_inference_all(wellness_states: dict, fuzzy_results: list, employees: list) -> list:
    """
    Run full inference for all employees.
    Returns list of dicts:
      {employee_id, name, actions, recommendations, symptom_check}
    """
    emp_names = {e["id"]: e["name"] for e in employees}
    fuzzy_map = {r["employee_id"]: r for r in fuzzy_results}

    results = []
    for emp_id, ws in wellness_states.items():
        fuzzy_out = fuzzy_map.get(emp_id, {
            "workload_reduction": 0.3,
            "schedule_flexibility": 0.3,
            "workload_label": "Low",
            "flexibility_label": "Low",
        })
        name = emp_names.get(emp_id, f"Employee {emp_id}")
        actions = derive_actions(ws, fuzzy_out)
        recs = generate_recommendations(ws, fuzzy_out, name)
        symptom = symptom_check(ws)

        results.append({
            "employee_id": emp_id,
            "name": name,
            "actions": actions,
            "recommendations": recs,
            "symptom_check": symptom,
        })
    return results

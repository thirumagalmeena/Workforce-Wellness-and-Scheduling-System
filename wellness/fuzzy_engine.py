"""
Pure-Python Fuzzy Logic Engine (no external library).

Uses triangular membership functions and Mamdani-style inference.

Inputs  (0-10 scale):
  - fatigue
  - stress
  - preference_match  (0: no match, 10: perfect match to preferred tasks)

Outputs (0-1 scale):
  - workload_reduction    (how much to lighten this employee's load)
  - schedule_flexibility  (how flexible the schedule should be)
"""

# ─── Membership Functions ────────────────────────────────────────────────────

def _trimf(x: float, a: float, b: float, c: float) -> float:
    """Triangular membership function over [a, b, c]."""
    if x <= a or x >= c:
        return 0.0
    if x <= b:
        return (x - a) / (b - a)
    return (c - x) / (c - b)


def _trapf(x: float, a: float, b: float, c: float, d: float) -> float:
    """Trapezoidal membership function over [a, b, c, d]."""
    if x <= a or x >= d:
        return 0.0
    if a < x < b:
        return (x - a) / (b - a)
    if b <= x <= c:
        return 1.0
    return (d - x) / (d - c)


# Fatigue / Stress linguistic levels (0–10)
def _low(x):    return _trapf(x, 0, 0, 2, 4)
def _medium(x): return _trimf(x, 2, 5, 8)
def _high(x):   return _trapf(x, 6, 8, 10, 10)

# Preference match (0–10)
def _pref_low(x):  return _trapf(x, 0, 0, 2, 5)
def _pref_high(x): return _trapf(x, 5, 8, 10, 10)


# ─── Defuzzification (centroid via discrete integration) ─────────────────────

def _defuzz_centroid(rules: list, universe=(0.0, 1.0), steps=100) -> float:
    """
    rules: list of (strength, output_center) tuples
    Returns centroid of aggregated activation.
    """
    lo, hi = universe
    step = (hi - lo) / steps
    num = 0.0
    denom = 0.0
    for xi in (lo + i * step for i in range(steps + 1)):
        # Aggregate: max of all rule activations clipped to their output center
        agg = 0.0
        for strength, center in rules:
            # Singleton representation: step function at center
            agg = max(agg, strength if abs(xi - center) < (1.0 / steps) * 2 else 0.0)
        num += xi * agg
        denom += agg
    return round(num / denom if denom > 0 else 0.3, 3)


# ─── Main Engine ─────────────────────────────────────────────────────────────

def evaluate(fatigue: float, stress: float, preference_match: float = 5.0) -> dict:
    """
    Evaluate fuzzy rules and return workload_reduction and schedule_flexibility.

    Example rule set (18 rules covering major combinations):
      R1: fatigue=HIGH  & stress=HIGH  → reduction=HIGH(0.9),  flex=HIGH(0.85)
      R2: fatigue=HIGH  & stress=MED   → reduction=MED(0.6),   flex=HIGH(0.75)
      R3: fatigue=MED   & stress=HIGH  → reduction=MED(0.55),  flex=HIGH(0.70)
      R4: fatigue=LOW   & stress=LOW   → reduction=LOW(0.1),   flex=LOW(0.2)
      R5: pref=LOW      & stress=MED   → reduction=MED(0.45),  flex=MED(0.5)
      R6: fatigue=HIGH  & pref=LOW     → reduction=HIGH(0.85), flex=HIGH(0.80)
      ... etc.
    """
    f_low    = _low(fatigue)
    f_med    = _medium(fatigue)
    f_high   = _high(fatigue)
    s_low    = _low(stress)
    s_med    = _medium(stress)
    s_high   = _high(stress)
    p_low    = _pref_low(preference_match)
    p_high   = _pref_high(preference_match)

    # Each rule: (activation_strength, output_center_for_reduction, center_for_flex)
    rules_reduction = [
        (min(f_high, s_high), 0.90),   # R1
        (min(f_high, s_med),  0.65),   # R2
        (min(f_med,  s_high), 0.60),   # R3
        (min(f_low,  s_low),  0.10),   # R4
        (min(f_low,  s_med),  0.25),   # R5
        (min(f_med,  s_low),  0.25),   # R6
        (min(f_high, p_low),  0.88),   # R7 — high fatigue + low pref match
        (min(f_med,  p_low),  0.50),   # R8
        (min(f_low,  p_high), 0.05),   # R9 — well-rested + prefers task
        (min(f_med,  s_med),  0.45),   # R10
    ]

    rules_flex = [
        (min(f_high, s_high), 0.90),
        (min(f_high, s_med),  0.75),
        (min(f_med,  s_high), 0.70),
        (min(f_low,  s_low),  0.20),
        (min(f_low,  s_med),  0.35),
        (min(f_med,  s_low),  0.30),
        (min(f_high, p_low),  0.85),
        (min(f_med,  p_low),  0.55),
        (min(f_low,  p_high), 0.10),
        (min(f_med,  s_med),  0.50),
    ]

    workload_reduction   = _defuzz_centroid(rules_reduction)
    schedule_flexibility = _defuzz_centroid(rules_flex)

    # Linguistic interpretation of output
    def _label(v):
        if v >= 0.7:   return "High"
        elif v >= 0.4: return "Medium"
        else:          return "Low"

    return {
        "workload_reduction":    workload_reduction,
        "schedule_flexibility":  schedule_flexibility,
        "workload_label":        _label(workload_reduction),
        "flexibility_label":     _label(schedule_flexibility),
        "fatigue_level":         "High" if f_high > 0.5 else ("Medium" if f_med > 0.5 else "Low"),
        "stress_level":          "High" if s_high > 0.5 else ("Medium" if s_med > 0.5 else "Low"),
    }


def evaluate_all(wellness_states: dict, employees: list) -> list:
    """Run fuzzy evaluation for all employees. Returns list of result dicts."""
    emp_names = {e["id"]: e["name"] for e in employees}
    results = []
    for emp_id, ws in wellness_states.items():
        # preference_match: rough proxy from high_priority_task_count (fewer = better match assumption)
        pref_match = max(0.0, 10.0 - ws["high_priority_task_count"] * 2.0)
        result = evaluate(ws["fatigue"], ws["stress"], pref_match)
        result["employee_id"] = emp_id
        result["name"] = emp_names.get(emp_id, f"Emp {emp_id}")
        results.append(result)
    return results

"""
Shift Rotation & Fairness Tracker.

Tracks long-term task distribution across employees and computes a
Gini-coefficient-based fairness score (0 = perfect equality, 1 = fully unfair).

Also exposes a fairness_penalty() for integration with the A* scheduler heuristic.
"""


class FairnessTracker:
    def __init__(self, employees):
        self.employees = employees
        self.emp_ids = [e["id"] for e in employees]
        # priority_load[emp_id] = sum of priority values assigned over all runs
        self.priority_load: dict[int, float] = {e: 0.0 for e in self.emp_ids}
        # total_hours[emp_id] = total scheduled hours over all runs
        self.total_hours: dict[int, float] = {e: 0.0 for e in self.emp_ids}
        # assignment history: list of {emp_id, task_id, priority, hours}
        self.history: list = []

    # ── Recording ────────────────────────────────────────────────────────────

    def record_assignments(self, schedule, tasks):
        """
        Update fairness history from a completed ScheduleState.
        Call this after each scheduler run.
        """
        task_priority = {t["id"]: t["priority"] for t in tasks}
        for task_id, (emp_id, start, end) in schedule.assignments.items():
            duration = end - start
            priority = task_priority.get(task_id, 1)
            self.priority_load[emp_id] = self.priority_load.get(emp_id, 0.0) + priority
            self.total_hours[emp_id]   = self.total_hours.get(emp_id, 0.0) + duration
            self.history.append({
                "employee_id": emp_id,
                "task_id": task_id,
                "priority": priority,
                "hours": duration,
            })

    # ── Gini Coefficient ─────────────────────────────────────────────────────

    @staticmethod
    def _gini(values: list) -> float:
        """Compute Gini coefficient for a list of non-negative values."""
        if not values or sum(values) == 0:
            return 0.0
        n = len(values)
        vals = sorted(values)
        cumsum = 0.0
        for i, v in enumerate(vals):
            cumsum += (2 * (i + 1) - n - 1) * v
        return cumsum / (n * sum(vals))

    # ── Fairness Scores ───────────────────────────────────────────────────────

    def compute_fairness_score(self) -> dict:
        """
        Returns:
          - gini_priority (0.0 = fair, 1.0 = totally unfair)
          - gini_hours
          - fairness_pct (0–100, higher = fairer)
          - per_employee breakdown
        """
        prio_vals  = [self.priority_load.get(e, 0.0) for e in self.emp_ids]
        hours_vals = [self.total_hours.get(e, 0.0)   for e in self.emp_ids]

        gini_p = round(self._gini(prio_vals), 3)
        gini_h = round(self._gini(hours_vals), 3)
        fairness_pct = round((1 - (gini_p + gini_h) / 2) * 100, 1)

        emp_names = {e["id"]: e["name"] for e in self.employees}
        per_employee = []
        for emp_id in self.emp_ids:
            per_employee.append({
                "employee_id": emp_id,
                "name": emp_names.get(emp_id, f"Emp {emp_id}"),
                "priority_load": round(self.priority_load.get(emp_id, 0.0), 2),
                "total_hours":   round(self.total_hours.get(emp_id, 0.0), 2),
            })
        # Sort by priority_load descending
        per_employee.sort(key=lambda x: x["priority_load"], reverse=True)

        return {
            "gini_priority": gini_p,
            "gini_hours": gini_h,
            "fairness_pct": fairness_pct,
            "per_employee": per_employee,
        }

    # ── Rotation Suggestions ─────────────────────────────────────────────────

    def get_rotation_suggestions(self) -> list:
        """
        Returns actionable rotation advice:
          - Employees with priority_load above average → assign lighter tasks next
          - Employees with priority_load below average → ready for heavier tasks
        """
        loads = [self.priority_load.get(e, 0.0) for e in self.emp_ids]
        if not loads:
            return []
        avg = sum(loads) / len(loads)
        emp_names = {e["id"]: e["name"] for e in self.employees}

        suggestions = []
        for emp_id in self.emp_ids:
            load = self.priority_load.get(emp_id, 0.0)
            name = emp_names.get(emp_id, f"Emp {emp_id}")
            if load > avg * 1.2:
                suggestions.append({
                    "employee_id": emp_id,
                    "name": name,
                    "suggestion": "lighter",
                    "message": f"🔄 {name}: priority load ({load:.1f}) is {((load/avg - 1)*100):.0f}% above average → assign lighter tasks next cycle.",
                })
            elif load < avg * 0.8:
                suggestions.append({
                    "employee_id": emp_id,
                    "name": name,
                    "suggestion": "heavier",
                    "message": f"⬆️  {name}: priority load ({load:.1f}) is {((1 - load/avg)*100):.0f}% below average → ready for higher-priority tasks.",
                })
            else:
                suggestions.append({
                    "employee_id": emp_id,
                    "name": name,
                    "suggestion": "balanced",
                    "message": f"✅ {name}: load is balanced ({load:.1f} ≈ avg {avg:.1f}).",
                })
        return suggestions

    # ── Heuristic Penalty for A* ─────────────────────────────────────────────

    def fairness_penalty(self, schedule, tasks) -> float:
        """
        Return a cost penalty for use in the A* heuristic:
        penalises assignments that concentrate high-priority tasks
        on already-overloaded employees.
        """
        task_priority = {t["id"]: t["priority"] for t in tasks}
        temp_load = dict(self.priority_load)

        for task_id, (emp_id, _, _) in schedule.assignments.items():
            priority = task_priority.get(task_id, 1)
            temp_load[emp_id] = temp_load.get(emp_id, 0.0) + priority

        # Variance across employees (higher = less fair)
        vals = list(temp_load.values())
        avg = sum(vals) / len(vals) if vals else 0
        variance = sum((v - avg) ** 2 for v in vals) / len(vals) if vals else 0
        return round(variance * 0.5, 2)   # scaled penalty

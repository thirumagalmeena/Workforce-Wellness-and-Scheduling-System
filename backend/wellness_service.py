"""
WellnessService — service layer for wellness operations.
Holds wellness state, fuzzy engine, inference engine, and fairness tracker.
"""
from wellness.wellness_model import default_wellness_states, update_from_schedule, make_wellness_state
from wellness.wellness_scorer import score_all_employees
from wellness.fuzzy_engine import evaluate_all
from wellness.inference_engine import run_inference_all
from wellness.fairness_tracker import FairnessTracker


class WellnessService:
    def __init__(self, employees, tasks):
        self.employees = employees
        self.tasks = tasks
        self.wellness_states = default_wellness_states(employees)
        self.fairness_tracker = FairnessTracker(employees)

    def update_employees(self, employees):
        """Called when employees list changes (e.g. after add_employee)."""
        self.employees = employees
        # Add wellness state for any new employees
        for emp in employees:
            if emp["id"] not in self.wellness_states:
                self.wellness_states[emp["id"]] = make_wellness_state(emp["id"])
        self.fairness_tracker = FairnessTracker(employees)

    def record_schedule(self, schedule):
        """Update wellness state and fairness tracker from a completed schedule."""
        if schedule:
            update_from_schedule(self.wellness_states, schedule, self.tasks)
            self.fairness_tracker.record_assignments(schedule, self.tasks)

    def update_wellness_signals(self, employee_id: int, fatigue: float = None,
                                 stress: float = None, satisfaction: float = None):
        """Manually update wellness signals for an employee (e.g. from frontend form)."""
        ws = self.wellness_states.get(employee_id)
        if ws is None:
            return {"error": f"Employee {employee_id} not found"}
        if fatigue is not None:
            ws["fatigue"] = max(0.0, min(10.0, fatigue))
        if stress is not None:
            ws["stress"] = max(0.0, min(10.0, stress))
        if satisfaction is not None:
            ws["satisfaction"] = max(0.0, min(10.0, satisfaction))
        return {"message": "Wellness signals updated", "employee_id": employee_id}

    def get_wellness_summary(self) -> list:
        """Return scored wellness data for all employees."""
        return score_all_employees(self.wellness_states, self.employees)

    def get_fuzzy_outputs(self) -> list:
        """Return fuzzy engine outputs for all employees."""
        return evaluate_all(self.wellness_states, self.employees)

    def get_recommendations(self) -> list:
        """Return inference engine results (actions + recommendations) for all employees."""
        fuzzy_results = self.get_fuzzy_outputs()
        return run_inference_all(self.wellness_states, fuzzy_results, self.employees)

    def get_fairness_report(self) -> dict:
        """Return fairness score and rotation suggestions."""
        return {
            "scores": self.fairness_tracker.compute_fairness_score(),
            "rotation_suggestions": self.fairness_tracker.get_rotation_suggestions(),
        }

    def reset(self, employees, tasks):
        """Reset all wellness state and fairness tracking."""
        self.employees = employees
        self.tasks = tasks
        self.wellness_states = default_wellness_states(employees)
        self.fairness_tracker = FairnessTracker(employees)

"""
Workforce Wellness & Scheduling System — CLI Demo
Run from project root:
    python main.py
"""

from core.data_loader import load_employees, load_tasks
from core.a_star_scheduler import AStarScheduler
from realtime.event_handler import employee_unavailable
from realtime.adjustment_search import AdjustmentSearch
from visualization.gantt_chart import plot_schedule

from wellness.wellness_model import default_wellness_states, update_from_schedule, make_wellness_state
from wellness.wellness_scorer import score_all_employees
from wellness.fuzzy_engine import evaluate_all
from wellness.inference_engine import run_inference_all
from wellness.fairness_tracker import FairnessTracker


def section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


# ==============================================================
# SECTION 1: Load Data & Initial Schedule
# ==============================================================
section("1. LOAD DATA & RUN INITIAL SCHEDULE")

employees = load_employees("data/employees.csv")
tasks     = load_tasks("data/tasks.csv")
tracker   = FairnessTracker(employees)

scheduler = AStarScheduler(employees, tasks)
schedule  = scheduler.solve()

if not schedule:
    print("  ⚠️  Scheduler could not find a valid schedule.")
else:
    print("\n  Initial Schedule:\n")
    for task_id, (emp, start, end) in schedule.assignments.items():
        emp_name  = next(e["name"] for e in employees if e["id"] == emp)
        task_name = next(t["name"] for t in tasks if t["id"] == task_id)
        print(f"    {task_name:25s} -> {emp_name:10s}  [{start:02d}:00 – {end:02d}:00]")

    tracker.record_assignments(schedule, tasks)


# ==============================================================
# SECTION 2: Simulate Event (Employee Unavailable)
# ==============================================================
section("2. REAL-TIME EVENT: Employee 1 Unavailable")

affected     = employee_unavailable(schedule, 1)
adjuster     = AdjustmentSearch(employees, tasks)
new_schedule, pending = adjuster.adjust(schedule, affected, 1)

print("\n  Updated Schedule:\n")
for task_id, (emp, start, end) in new_schedule.assignments.items():
    emp_name  = next(e["name"] for e in employees if e["id"] == emp)
    task_name = next(t["name"] for t in tasks if t["id"] == task_id)
    print(f"    {task_name:25s} -> {emp_name:10s}  [{start:02d}:00 – {end:02d}:00]")

if pending:
    print(f"\n  Pending Queue: {pending}")
else:
    print("\n  All tasks successfully reassigned.")


# ==============================================================
# SECTION 3: Wellness Model — Simulate Signals
# ==============================================================
section("3. WELLNESS MODEL — Deriving States from Schedule")

wellness_states = default_wellness_states(employees)

# Simulate real-world variation: some employees more stressed
wellness_states[1]["fatigue"] = 7.5   # Alice overworked
wellness_states[1]["stress"]  = 6.5
wellness_states[2]["fatigue"] = 3.0   # Bob doing well
wellness_states[2]["satisfaction"] = 8.0
wellness_states[3]["consecutive_shifts"] = 6   # Carol near limit
wellness_states[4]["high_priority_task_count"] = 4   # David loaded

# Also update from the actual schedule run
update_from_schedule(wellness_states, new_schedule, tasks)

print("\n  Wellness State Summary:\n")
print(f"  {'Employee':<12} {'Fatigue':>8} {'Stress':>8} {'Satisf.':>9} {'Consec.Shifts':>14} {'WklyHrs':>9}")
print("  " + "-"*58)
for emp in employees:
    ws = wellness_states[emp["id"]]
    print(
        f"  {emp['name']:<12} {ws['fatigue']:>8.1f} {ws['stress']:>8.1f} "
        f"{ws['satisfaction']:>9.1f} {ws['consecutive_shifts']:>14} {ws['weekly_hours']:>9.1f}"
    )


# ==============================================================
# SECTION 4: Wellness Scorer
# ==============================================================
section("4. WELLNESS SCORER — Compute Scores & Tags")

scores = score_all_employees(wellness_states, employees)

print(f"\n  {'Employee':<12} {'Score':>7} {'Tag':<12} {'Fatigue Pen':>12} {'Stress Pen':>11}")
print("  " + "-"*58)
for s in scores:
    print(
        f"  {s['name']:<12} {s['score']:>7.1f} {s['tag']:<12} "
        f"{s['breakdown']['fatigue_penalty']:>12.1f} {s['breakdown']['stress_penalty']:>11.1f}"
    )


# ==============================================================
# SECTION 5: Fuzzy Logic Engine
# ==============================================================
section("5. FUZZY LOGIC ENGINE — Workload & Flexibility Analysis")

fuzzy_results = evaluate_all(wellness_states, employees)

print(f"\n  {'Employee':<12} {'Wkld Reduc.':>13} {'Flex.':>7} {'Fatigue':>9} {'Stress':>8}")
print("  " + "-"*54)
for r in fuzzy_results:
    print(
        f"  {r['name']:<12} {r['workload_label']:>13} ({r['workload_reduction']:.2f})"
        f"  {r['flexibility_label']:>7}  {r['fatigue_level']:>9}  {r['stress_level']:>8}"
    )


# ==============================================================
# SECTION 6: Inference Engine — Actions & Recommendations
# ==============================================================
section("6. INFERENCE ENGINE — Actions & Recommendations")

inference_results = run_inference_all(wellness_states, fuzzy_results, employees)

for emp_result in inference_results:
    print(f"\n  -- {emp_result['name']} -----------------------------")
    print(f"     Actions: {', '.join(emp_result['actions'])}")
    for rec in emp_result["recommendations"]:
        # Wrap long lines
        print(f"     {rec}")
    sc = emp_result["symptom_check"]
    print(f"     {sc['message']}")


# ==============================================================
# SECTION 7: Fairness Tracker — Gini & Rotation Suggestions
# ==============================================================
section("7. FAIRNESS TRACKER — Gini Coefficient & Rotation")

fairness = tracker.compute_fairness_score()
print(f"\n  Gini (Priority):  {fairness['gini_priority']:.3f}   (0.0 = perfectly fair)")
print(f"  Gini (Hours):     {fairness['gini_hours']:.3f}")
print(f"  Fairness Score:   {fairness['fairness_pct']}%\n")

print("  Per-Employee Load:\n")
print(f"  {'Name':<12} {'Priority Load':>14} {'Total Hours':>12}")
print("  " + "-"*40)
for e in fairness["per_employee"]:
    print(f"  {e['name']:<12} {e['priority_load']:>14.2f} {e['total_hours']:>12.2f}")

print("\n  Rotation Suggestions:\n")
for s in tracker.get_rotation_suggestions():
    print(f"  {s['message']}")


# ==============================================================
# SECTION 8: Manual Reassignment Override
# ==============================================================
section("8. MANUAL REASSIGNMENT OVERRIDE")

print("  Simulating manager explicitly overriding the AI to assign a pending task.")
# Find a pending task
assigned_task_ids = set(new_schedule.assignments.keys())
pending_tasks = [t for t in tasks if t["id"] not in assigned_task_ids]

if pending_tasks:
    target_task = pending_tasks[0]
    # Find an idle employee if any, else just use Employee 5 (Eve)
    assigned_emp_ids = set(emp for emp, _, _ in new_schedule.assignments.values())
    idle_emps = [e for e in employees if e["id"] not in assigned_emp_ids]
    
    target_emp = idle_emps[0] if idle_emps else employees[-1]
    
    print(f"\n  Manager assigns: [{target_task['name']}] to [{target_emp['name']}]")
    
    # Re-run A* with manual injection
    scheduler = AStarScheduler(employees, tasks, manual_assignments={
        target_task["id"]: {
            "employee_id": target_emp["id"],
            "start": target_emp["available_from"],
            "end": target_emp["available_from"] + target_task["duration"]
        }
    })
    
    overridden_schedule = scheduler.solve()
    
    if overridden_schedule:
        print("\n  Updated Schedule (After Override):\n")
        new_assigned_ids = set(overridden_schedule.assignments.keys())
        for task_id, (emp, start, end) in overridden_schedule.assignments.items():
            emp_name  = next(e["name"] for e in employees if e["id"] == emp)
            t_name = next(t["name"] for t in tasks if t["id"] == task_id)
            if task_id == target_task["id"]:
                print(f"  * {t_name:25s} -> {emp_name:10s}  [{start:02d}:00 - {end:02d}:00]  <-- MANUAL")
            else:
                print(f"    {t_name:25s} -> {emp_name:10s}  [{start:02d}:00 - {end:02d}:00]")
                
        new_pending = [t for t in tasks if t["id"] not in new_assigned_ids]
        print(f"\n  Pending Queue remaining: {len(new_pending)}")
        
        # We'll use the overridden schedule for the Gantt chart
        new_schedule = overridden_schedule
    else:
        print("  Override failed constraints (e.g. employee lacks skills).")
else:
    print("  No pending tasks to manually assign.")

# ==============================================================
# SECTION 9: Gantt Chart
# ==============================================================
section("9. GANTT CHART (closing window continues CLI)")
plot_schedule(new_schedule, employees, tasks)
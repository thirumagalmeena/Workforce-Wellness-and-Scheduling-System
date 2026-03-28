from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from backend.scheduler_service import SchedulerService

app = FastAPI(title="Workforce Wellness & Scheduling API")
service = SchedulerService()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Schedule Endpoints ───────────────────────────────────────────────────────

@app.get("/schedule")
def get_schedule():
    return service.get_schedule()

@app.post("/add-employee")
def add_employee(emp: dict):
    service.add_employee(emp)
    return {"message": "Employee added"}

@app.post("/add-task")
def add_task(task: dict):
    service.add_task(task)
    return {"message": "Task added"}

@app.post("/reschedule")
def reschedule():
    service.run_scheduler()
    return service.get_schedule()

@app.post("/simulate-event")
def simulate_event(employee_id: int):
    return service.handle_employee_unavailable(employee_id)

@app.post("/reset")
def reset_data():
    return service.reset()

class ReassignUpdate(BaseModel):
    task_id: int
    employee_id: int

@app.post("/reassign-task")
def reassign_task(payload: ReassignUpdate):
    return service.reassign_task(payload.task_id, payload.employee_id)

# ─── Wellness Endpoints ───────────────────────────────────────────────────────

@app.get("/wellness")
def get_wellness():
    """Returns wellness score, tag, and signal breakdown for all employees."""
    return {"wellness": service.get_wellness_summary()}

@app.get("/fairness")
def get_fairness():
    """Returns Gini fairness scores and rotation suggestions."""
    return service.get_fairness_report()

@app.get("/recommendations")
def get_recommendations():
    """Returns inference engine recommendations per employee."""
    return {"recommendations": service.get_recommendations()}


class WellnessUpdate(BaseModel):
    employee_id: int
    fatigue: Optional[float] = None
    stress: Optional[float] = None
    satisfaction: Optional[float] = None

@app.post("/update-wellness")
def update_wellness(payload: WellnessUpdate):
    """Manually update wellness signals for an employee."""
    return service.update_wellness_signals(
        payload.employee_id,
        fatigue=payload.fatigue,
        stress=payload.stress,
        satisfaction=payload.satisfaction,
    )
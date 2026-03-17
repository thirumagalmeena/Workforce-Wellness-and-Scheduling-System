from fastapi import FastAPI
from backend.scheduler_service import SchedulerService
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
service = SchedulerService()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    """Reset to default data from CSV files"""
    return service.reset()
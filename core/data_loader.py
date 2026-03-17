import pandas as pd

def load_employees(path):
    df = pd.read_csv(path)

    employees = []
    for _, row in df.iterrows():
        employees.append({
            "id": row["employee_id"],
            "name": row["name"],
            "skills": row["skills"].split("|"),
            "available_from": row["available_from"],
            "available_to": row["available_to"],
            "max_hours": row["max_hours_per_day"],
            "preferred_tasks": row["preferred_tasks"]
        })

    return employees


def load_tasks(path):
    df = pd.read_csv(path)

    tasks = []
    for _, row in df.iterrows():
        tasks.append({
            "id": row["task_id"],
            "name": row["task_name"],
            "skill": row["required_skill"],
            "duration": row["duration"],
            "deadline": row["deadline"],
            "priority": row["priority"]
        })

    tasks.sort(key=lambda x: x["priority"])#, reverse=True)

    return tasks
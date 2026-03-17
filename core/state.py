class ScheduleState:
    def __init__(self):
        self.assignments = {}

    def add(self, task_id, employee_id, start, end):
        self.assignments[task_id] = (employee_id, start, end)

    def remove(self, task_id):
        if task_id in self.assignments:
            del self.assignments[task_id]

    def get_employee_tasks(self, employee_id):
        tasks = []
        for task, (emp, start, end) in self.assignments.items():
            if emp == employee_id:
                tasks.append((task, start, end))
        return tasks

    def __str__(self):
        return str(self.assignments)
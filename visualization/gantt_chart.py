import matplotlib.pyplot as plt


def plot_schedule(schedule, employees, tasks):

    employee_names = {e["id"]: e["name"] for e in employees}
    task_names = {t["id"]: t["name"] for t in tasks}

    fig, ax = plt.subplots()

    for task_id, (emp, start, end) in schedule.assignments.items():

        ax.barh(
            employee_names[emp],
            end - start,
            left=start
        )

        ax.text(
            start,
            employee_names[emp],
            task_names[task_id]
        )

    ax.set_xlabel("Time")
    ax.set_title("Employee Schedule")

    plt.show()
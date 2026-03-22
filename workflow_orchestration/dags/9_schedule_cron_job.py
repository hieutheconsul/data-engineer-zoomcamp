from airflow.sdk import dag, task
from pendulum import datetime, duration
from airflow.timetables.trigger import DeltaTriggerTimetable

@dag(
        dag_id="schedule_delta",
        start_date = datetime(year=2026, month=1, day=26, tz="Asia/Ho_Chi_Minh"),
        schedule=DeltaTriggerTimetable(duration(days=3)),
        end_date = datetime(year=2026, month=1, day=31, tz="Asia/Ho_Chi_Minh"),
        is_paused_upon_creation=False,
        catchup=True
)

def schedule_delta():

    @task.python
    def first_task():
        print("This is my first task")

    @task.python
    def second_task():
        print("This is my second task")

    @task.python
    def third_task():
        print("This is my third task")

    # Defining task dependencies
    first = first_task()
    second = second_task()
    third = third_task()

    # Sequence (at DAG level, not each task's level)
    first >> second >> third

# Instantiating the DAG
schedule_delta()
from airflow.sdk import dag, task

@dag(
        dag_id="first_dag"
)

def first_dag():

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
first_dag()
from airflow.sdk import dag, task

@dag(
        dag_id="versioned_dag"
)

def versioned_dag():

    @task.python
    def first_task():
        print("This is my first task")

    @task.python
    def second_task():
        print("This is my second task")

    @task.python
    def third_task():
        print("This is my third task")

    @task.python
    def version_task():
        print("This is the version task. DAG version 2.0")

    # Defining task dependencies
    first = first_task()
    second = second_task()
    third = third_task()
    version = version_task()

    # Sequence (at DAG level, not each task's level)
    first >> second >> third >> version

# Instantiating the DAG
versioned_dag()
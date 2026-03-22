from airflow.sdk import dag, task
from airflow.operators.bash import BashOperator

@dag(
        dag_id="operators_dag"
)

def operators_dag():

    @task.python
    def first_task():
        print("This is my first task")

    @task.python
    def second_task():
        print("This is my second task")

    @task.bash
    def bash_task_modern():
        return "echo http://airflow.apache.org/"

    bash_task_old = BashOperator(
        task_id = "bash_task_old",
        bash_command = "echo http://airflow.apache.org/"
    )
    # Defining task dependencies
    first = first_task()
    second = second_task()
    bash_modern = bash_task_modern()
    bash_old = bash_task_old

    # Sequence (at DAG level, not each task's level)
    first >> second >> bash_modern >> bash_old

# Instantiating the DAG
operators_dag()
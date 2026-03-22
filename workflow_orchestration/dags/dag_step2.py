from airflow.sdk import dag, task
import os

@dag(
        dag_id="dag_step2"
)

def dag_step2():

    @task.python
    def first_task():
        print("This is my first task")

    @task.python
    def second_task():
        print("This is my second task")

    @task.python
    def third_task():
        #Ensure the directory exists
        os.makedirs(os.path.dirname("/opt/airflow/logs/data"), exist_ok=True)

        #Simulate data fetching by writing to a file
        with open("/opt/airflow/logs/data/ouput_dag_step2.txt", 'w') as f:
            f.write(f"Data processed successfully")

    # Defining task dependencies
    first = first_task()
    second = second_task()
    third = third_task()

    # Sequence (at DAG level, not each task's level)
    first >> second >> third

# Instantiating the DAG
dag_step2()
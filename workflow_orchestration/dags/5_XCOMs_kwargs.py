from airflow.sdk import dag, task

@dag(
        dag_id="xcoms_dag_kwargs"
)

def xcoms_dag_kwargs():

    @task.python
    def first_task(**kwargs):

        #Extracting 'ti' from kwargs to push XCOMs manually
        ti = kwargs['ti']

        print("Extracting data...")
        fetched_data = {"data": [1, 2, 3, 4, 5]}
        ti.xcom_push(key='first_task_output', value = fetched_data) #actively push data to XCOMs

    @task.python
    def second_task(**kwargs):
        ti = kwargs['ti']
        print("Transforming data...")
        #Pulling XCOMs pushed from first task
        fetched_data = ti.xcom_pull(task_ids = 'first_task', key = 'first_task_output')['data']

        transformed_data = fetched_data*2
        transformed_data_dict = {"transf_data":transformed_data}
        ti.xcom_push(key='second_task_output', value = transformed_data_dict)

    @task.python
    def third_task(**kwargs):
        ti = kwargs['ti']
        print("Loading data...")
        load_data = ti.xcom_pull(task_ids = 'second_task', key = 'second_task_output')
        return load_data

    # Defining task dependencies
    first = first_task()
    second = second_task()
    third = third_task()

    # Sequence (at DAG level, not each task's level)
    first >> second >> third #must have if doing manual push/pull

# Instantiating the DAG
xcoms_dag_kwargs()
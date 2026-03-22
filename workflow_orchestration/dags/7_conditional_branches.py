from airflow.sdk import dag, task

@dag(
        dag_id="conditional_branch_dags"
)

def conditional_branch_dags():

    @task.python
    def extract_task(**kwargs):
        print("Extracting...")
        ti = kwargs['ti']
        extracted_data_dict = {"api_extracted_data" : [1,2,3],
                               "db_extracted_data" : [4,5,6],
                               "s3_extracted_data" : [7,8,9],
                               "weekend_flag" : "false"}
        ti.xcom_push(key = 'return_value', value = extracted_data_dict)

    @task.python
    def transform_task_api(**kwargs):
        ti = kwargs['ti']
        print("Transforming API task...")
        api_extracted_data = ti.xcom_pull(task_ids='extract_task')['api_extracted_data']
        transformed_api_data = [i*10 for i in api_extracted_data]
        ti.xcom_push(key='return_api_value', value=transformed_api_data)

    @task.python
    def transform_task_db(**kwargs):
        ti = kwargs['ti']
        print("Transforming DB task...")
        db_extracted_data = ti.xcom_pull(task_ids='extract_task')['db_extracted_data']
        transformed_db_data = [i*100 for i in db_extracted_data]
        ti.xcom_push(key='return_api_value', value=transformed_db_data)

    @task.python
    def transform_task_s3(**kwargs):
        ti = kwargs['ti']
        print("Transforming S3 task...")
        s3_extracted_data = ti.xcom_pull(task_ids='extract_task')['s3_extracted_data']
        transformed_s3_data = [i*1000 for i in s3_extracted_data]
        ti.xcom_push(key='return_s3_value', value=transformed_s3_data)

    #Creating Conditional Node
    @task.branch
    def conditional_node(**kwargs):
        ti = kwargs['ti']
        weekend_flag = ti.xcom_pull(task_ids = 'extract_task')['weekend_flag']
        if weekend_flag == "true" :
            return 'no_load_task'
        else:
            return 'load_task'

    @task.bash
    def load_task(**kwargs):
        print("Loading data to destination...")
        api_data = kwargs['ti'].xcom_pull(task_ids='transform_task_api')
        db_data = kwargs['ti'].xcom_pull(task_ids='transform_task_db')
        s3_data = kwargs['ti'].xcom_pull(task_ids='transform_task_s3')

        return f"echo 'Loaded Data: {api_data}, {db_data}, {s3_data}'"
    
    @task.bash
    def no_load_task(**kwargs):
        print("No loading task on weekend...")
        return f"echo 'Not loading data'"

    # Defining task dependencies
    extract = extract_task()
    transform_api = transform_task_api()
    transform_db = transform_task_db()
    transform_s3 = transform_task_s3()
    load = load_task()
    no_load = no_load_task()

    # Sequence (at DAG level, not each task's level)
    extract >> [transform_api, transform_db, transform_s3] >> conditional_node() >> [load, no_load]

# Instantiating the DAG
conditional_branch_dags()
from airflow.sdk import dag, task
from dag_step1 import dag_step1
from dag_step2 import dag_step2
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

@dag(
        dag_id="dag_combined"
)

def dag_combined():

    trigger_dag_step1 = TriggerDagRunOperator(
        task_id="trigger_dag_step1",
        trigger_dag_id="dag_step1",
        wait_for_completion=True
    )
    trigger_dag_step2 = TriggerDagRunOperator(
        task_id="trigger_dag_step2",
        trigger_dag_id="dag_step2",
        wait_for_completion=True
    )

    trigger_dag_step1 >> trigger_dag_step2
    
# Instantiating the DAG
dag_combined()
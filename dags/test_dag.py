from airflow import DAG
import datetime as dt
from airflow.operators.bash import BashOperator

with DAG(
        dag_id="test",
        start_date=dt.datetime(2022, 10, 1),
        schedule_interval=None,
        catchup=False
) as dag:
    example = BashOperator(
        task_id='teste',
        bash_command='echo pwd'
    )

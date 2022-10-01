import ast

from airflow import DAG
import datetime as dt
from decouple import config
from discord_webhook import DiscordWebhook

from dags.airflow_currecy.request_currency import execute
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator

headers = {
    "X-RapidAPI-Key": config('KEY'),
    "X-RapidAPI-Host": config('HOST')
}


def send_msg(msg):
    payload = ast.literal_eval(msg)
    rates = payload.get('rates')
    symbols = [key for key in rates.keys()]
    msg_discord = f"""Fetching {", ".join(str(x) for x in symbols)} !!! The currency at {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} is: \n"""

    for key in rates:
        msg_discord += f'''\t{key}: {round(rates.get(key), 3)}\n'''

    webhook = DiscordWebhook(url=config('WEBHOOK'),rate_limit_retry=True,content=msg_discord)
    webhook.execute()


with DAG(
        dag_id="currency",
        description="Fetches currency of Iene, Euro and Pound",
        start_date=dt.datetime(2022, 10, 1),
        schedule_interval="30 * * * *",
        catchup=False
) as dag:
    star_dag = DummyOperator(task_id='begin')

    fetch_currency = PythonOperator(task_id='fetching',
                                    python_callable=execute,
                                    op_kwargs={
                                        'base': "USD",
                                        'symbols': ["GBP", "JPY", "EUR"],
                                        'headers': headers
                                    },
                                    do_xcom_push=True)

    send_msg_discord = PythonOperator(task_id='msg',
                                      python_callable=send_msg,
                                      op_kwargs={
                                          'msg': "{{task_instance.xcom_pull(task_ids='fetching')}}"
                                      },
                                      do_xcom_push=True)

    end_dag = DummyOperator(task_id='end')

star_dag >> fetch_currency >> send_msg_discord >> end_dag

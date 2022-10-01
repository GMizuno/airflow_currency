from dags.airflow_currecy import execute
from decouple import config

headers = {
    "X-RapidAPI-Key": config('KEY'),
    "X-RapidAPI-Host": config('HOST')
}

print(execute("USD", ["GBP", "JPY", "EUR"], headers=headers))

d = {'timestamp': '2022-10-01 19:49:04', 'base': 'USD', 'rates': {'GBP': 0.896861, 'JPY': 144.73904, 'EUR': 1.01991}}
r = d.get('rates')
msg = ' test\n'
for key in r:
    msg += f'''{key}: {r.get(key)}\n'''
print(msg)

import datetime

from celery import Celery

app = Celery('task', broker= 'pyamqp://guest@localhost//')

@app.task
def add(x, y):
    with open('test.txt', 'w') as f:
        f.write(f'x + y = {x + y} {datetime.datetime.now()}')
    return x + y


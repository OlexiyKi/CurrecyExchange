import datetime

from celery import Celery
from celery.schedules import crontab

app = Celery('celery_working', broker= 'pyamqp://guest@localhost//')

#to run: celery -A celery_working worker --loglevel=INFO -B
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    #calls func every 10 sec
    sender.add_periodic_task(10.0, add.s(x=2, y=4), name='add every 10')


@app.task
def add(x, y):
    with open('test.txt', 'w') as f:
        f.write(f'x + y = {x + y} {datetime.datetime.now()}')
    return x + y


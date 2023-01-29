import datetime
import os

from celery import Celery
from celery.schedules import crontab
import models_db
import al_db
from sqlalchemy.orm import Session


rabbit_host = os.environ.get('RABBIT_HOST', 'localhost')
app = Celery('celery_working', broker= f'pyamqp://guest@{rabbit_host}//')

#to run: celery -A celery_working worker --loglevel=INFO -B
# -B это параметр, который запускает add_periodic_task()
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    #calls func every 10 sec
    sender.add_periodic_task(10.0, add.s(x=2, y=4), name='add every 10')


@app.task
def add(x, y):
    record_1 = models_db.Currency(bank='NewBank', currency="BNB", date_exchange='2023-01-01', buy_rate=1.3,
                                  sale_rate=11)
    with Session(al_db.engine) as session:
        session.add(record_1)
        session.commit()
    return x + y


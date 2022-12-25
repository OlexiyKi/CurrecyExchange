# syntax=docker/dockerfile:1

FROM python:3.11

WORKDIR /exchange_rate_app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "app.py"]

#sudo docker build --tag python-docker .
#celery -A celery_working worker --loglevel=INFO -B   (запускает beat (-B) из воркера)
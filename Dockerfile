# syntax=docker/dockerfile:1

FROM python:3.11

WORKDIR /exchange_rate_app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .



#sudo docker build --tag python-docker .    #build image with our app
#celery -A celery_working worker --loglevel=INFO -B   (запускает beat (-B) из воркера)
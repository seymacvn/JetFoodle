FROM python:3.8.5

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

ADD requirements.txt /usr/src/app

RUN pip install --upgrade pip && pip install -r requirements.txt


FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir /long_task

WORKDIR /long_task

ADD . /long_task/

RUN python -m pip install -r requirements.txt



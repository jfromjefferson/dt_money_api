# syntax=docker/dockerfile:1

FROM python:3.10
WORKDIR /dt_money/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . /dt_money/

RUN apt update 
RUN pip install -r requirements.txt
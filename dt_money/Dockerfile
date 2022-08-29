# syntax=docker/dockerfile:1

FROM python:latest
WORKDIR /dt_money/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . /dt_money/

RUN apt update 
RUN pip install -r requirements.txt
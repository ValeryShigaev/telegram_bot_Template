FROM python:3.11.3-slim

RUN pip3 install --upgrade pip

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY . .
RUN pip3 install -r requirements.txt
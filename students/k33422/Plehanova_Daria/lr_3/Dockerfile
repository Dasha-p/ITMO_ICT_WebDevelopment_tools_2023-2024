FROM python:3.11.9-slim-bookworm

WORKDIR /application

COPY requirements.txt .

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

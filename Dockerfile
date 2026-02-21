FROM python:3.11-slim-bullseye AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x scripts/start_*.sh

ENV PYTHONPATH="/app/src"

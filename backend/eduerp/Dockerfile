# backend/Dockerfile
FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        gcc \
        libpq-dev \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements/production.txt .
RUN pip install --no-cache-dir -r production.txt

COPY . .

RUN mkdir -p /app/logs && touch /app/logs/eduerp.log
RUN chmod -R 755 /app/logs

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "config.wsgi:application"]
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.8.3
RUN pip install "poetry==${POETRY_VERSION}"

COPY pyproject.toml /app/
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY worker.py /app/worker.py

CMD ["celery", "-A", "worker.app", "worker", "--loglevel=INFO"]


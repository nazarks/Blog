FROM python:3.10-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
ENV POETRY_VERSION=1.3.1

RUN apt-get update \
    && apt-get install -y postgresql postgresql-contrib libpq-dev python3-dev

RUN pip install poetry==$POETRY_VERSION

WORKDIR /app

COPY development.env production.env ./
COPY poetry.lock pyproject.toml ./
COPY wsgi.py ./
COPY migrations ./migrations

RUN poetry export -f requirements.txt --output requirements.txt
RUN pip install --no-cache -r requirements.txt

COPY blog ./blog

COPY var/scripts/wait-for-postgres.sh .
RUN chmod +x wait-for-postgres.sh

EXPOSE 5000
# CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]

FROM python:3.12 AS builder
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN python -m venv env
ENV PATH="/app/env/bin:$PATH"

COPY ./requirements/production.txt ./requirements.txt
ENV PIP_DEFAULT_TIMEOUT=300
RUN pip install -r requirements.txt


FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y libpq-dev gcc postgresql-client cron

WORKDIR /app

COPY --from=builder /app/env ./env/
ENV PATH="/app/env/bin:$PATH"

COPY ./src ./src/
WORKDIR /app/src

COPY ./infrastructure/entrypoint.sh .

EXPOSE 8000
CMD ["./entrypoint.sh"]

FROM python:3.11

EXPOSE 8001

ENV PYTHONUNBUFFERED=1

WORKDIR /law_office

COPY pyproject.toml poetry.lock /law_office/

RUN pip3 install poetry && poetry install --no-cache

COPY . .

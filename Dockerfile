FROM python:3.10-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR  /app

RUN apt-get update && \
    apt install -y python3-dev

RUN pip3 install --upgrade pip
RUN pip3 install poetry
ADD pyproject.toml .
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

EXPOSE 8000

COPY . .

RUN chmod a+x /app/docker/*.sh

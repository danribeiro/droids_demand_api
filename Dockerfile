# pull official base image
FROM python:3.8.3-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
COPY entrypoint.sh /entrypoint.sh
RUN pip install -r requirements.txt
RUN chmod +x /entrypoint.sh

COPY . .
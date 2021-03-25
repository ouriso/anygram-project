FROM python:3.8.5

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./src/requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY ./src .
COPY ./nginx /nginx
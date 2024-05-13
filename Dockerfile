FROM python:3.12.2-slim-bullseye

WORKDIR /app

RUN apt update && apt install git -y

COPY ./requirements.txt ./

RUN pip install -r ./requirements.txt

# src klasörü içerisindeki herşeyi /app klasörüne kopyala
COPY ./src/ .
EXPOSE 8000
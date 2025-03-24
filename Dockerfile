FROM python:3.10.5-slim-buster

RUN pip install --upgrade pip

RUN apt update
RUN apt install  libopus0 libopus-dev
RUN apt-get update && apt-get install -y ffmpeg

COPY ./requirements.txt .
RUN pip install ffmpeg-python
RUN pip install -r requirements.txt

COPY . /app

RUN ls .
WORKDIR /app/
#CMD exec python bot.py
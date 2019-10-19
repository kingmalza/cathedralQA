
FROM python:3.6-alpine
#ENV PYTHONUNBUFFERED 1
RUN apk add --no-cache make linux-headers libffi-dev jpeg-dev zlib-dev
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
#RUN apk update && apk add build-essential libssl-dev libffi-dev
RUN mkdir /Code
WORKDIR /Code
COPY ./requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED 1

COPY . /Code/
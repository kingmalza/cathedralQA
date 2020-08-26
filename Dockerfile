
#FROM python:3.6
#EXPOSE 8000
#RUN apt-get update
#RUN apt-get install -y \
#        make linux-headers-amd64 libffi-dev libjpeg-dev libz-dev \
#        postgresql-server-dev-11 gcc python3-dev musl-dev \
#    && rm -rf /var/lib/apt/lists/*

FROM python:3.6-alpine
EXPOSE 8000
RUN apk update
RUN apk add --no-cache make linux-headers libffi-dev jpeg-dev zlib-dev
RUN apk add postgresql-dev gcc python3-dev musl-dev

#RUN mkdir /Code

VOLUME /var/lib/cathstudio/data
WORKDIR /var/lib/cathstudio/data

COPY ./requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /var/lib/cathstudio/data

COPY . /var/lib/cathstudio/data

RUN python -m compileall -b ajaxfuncs/

ENTRYPOINT python core/manage.py runserver 0.0.0.0:8000


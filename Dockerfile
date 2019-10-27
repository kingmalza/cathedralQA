
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
RUN mkdir /Code

#VOLUME /var/lib/cathstudio/data
WORKDIR /Code

COPY ./requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED 1

COPY . /Code/

RUN python -m compileall /Code/ajaxfuncs/
RUN python -m compileall /Code/core/core/
RUN python -m compileall /Code/rsthtml/

#RUN rm -rf /Code/core/*.py !manage.py
RUN rm -rf /Code/ajaxfuncs/*.py
#RUN rm -rf /Code/rsthtml/*.py

ENTRYPOINT python /Code/core/manage.py runserver 0.0.0.0:8000


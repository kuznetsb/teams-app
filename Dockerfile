FROM python:3.11.1-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
COPY . .

RUN apk --update add libxml2-dev libxslt-dev libffi-dev gcc \
     musl-dev libgcc openssl-dev curl
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev \
    tiff-dev tk-dev tcl-dev

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1

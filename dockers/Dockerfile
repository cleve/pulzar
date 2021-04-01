FROM ubuntu:20.04

LABEL maintainer="mauricio.cleveland@gmail.com" version="21.4.1" build_date="2021-04-01"

ENV DEBIAN_FRONTEND=nonintercative
ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1
RUN apt update && apt -y upgrade && \
    apt -y install build-essential python3-pip nano tesseract-ocr libopencv-dev python3-opencv

RUN mkdir /var/lib/pulzar /var/lib/pulzar/data /var/lib/pulzar/dbs /var/lib/pulzar/config /var/lib/pulzar/log /usr/local/bin/pulzar
COPY dockers/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
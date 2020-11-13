FROM ubuntu:20.04

LABEL maintainer="mcleveland@comscore.com"
LABEL build_date="2020-11-13"

EXPOSE 31415
ENV DEBIAN_FRONTEND=nonintercative
ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1
RUN apt update && apt -y upgrade && \
    apt -y install build-essential python3-pip libffi-dev nano unixodbc-dev tesseract-ocr libopencv-dev python3-opencv

RUN mkdir /var/lib/pulzar
RUN mkdir /var/lib/pulzar/data
RUN mkdir /var/lib/pulzar/dbs
RUN mkdir /var/lib/pulzar/config
RUN mkdir /usr/local/bin/pulzar
COPY dockers/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
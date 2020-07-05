FROM alpine:3.12.0

LABEL Mauricio Cleveland "mauricio.cleveland@gmail.com"

EXPOSE 9000
VOLUME /usr/src/app/public
WORKDIR /usr/src/app
RUN apk add python3-dev build-base linux-headers pcre-dev
RUN apk add --no-cache \
    python3 \
    py3-pip
COPY app .
COPY requirements.txt requirements.txt
RUN rm -rf public/*
RUN pip3 install --no-cache-dir -r requirements.txt
CMD [ "uwsgi", "-i", "config/master.ini" ]
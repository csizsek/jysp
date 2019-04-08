FROM python:3.7-alpine

RUN apk add --no-cache python py-pip build-base ruby-rake
RUN rm -rf /var/cache/apk/*

ADD requirements.txt requirements.txt
RUN pip3.7 install -r requirements.txt
RUN rm requirements.txt
FROM python:3.6-stretch

RUN mkdir /app
WORKDIR /app

RUN pip3 install Scrapy==1.6.0

ADD . .
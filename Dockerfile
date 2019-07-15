FROM python:3.6-stretch

WORKDIR /opt/avere-europarl

RUN pip3 install Scrapy==1.6.0

ADD LICENSE README.md ./
ADD scraper ./scraper

CMD cd scraper && ./main.py
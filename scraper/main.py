#!/usr/bin/python3

from scrapy.crawler import CrawlerProcess
from scraper.spiders.meps import XMLParser, MEPSCrawler
from scrapy.utils.project import get_project_settings
import logging

BASE_URL = 'https://www.europarl.europa.eu/meps/en/'


def main():
    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(XMLParser)
    logging.info("Starting xml crawler")
    process.start()
    logging.info("Finished crawling xml")

    with open("links.csv") as f:
        for line in f.readlines():
            full_name, id = line.split(',')
            url = BASE_URL + id
            process.crawl(MEPSCrawler, url=url)
            return 0


if __name__ == '__main__':
    main()

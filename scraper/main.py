#!/usr/bin/python3

from scrapy.crawler import CrawlerRunner
from scraper.spiders.meps import XMLParser, MEPSCrawler
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
from twisted.internet import reactor, defer

import csv

BASE_URL = 'https://www.europarl.europa.eu/meps/en/'


@defer.inlineCallbacks
def crawl(runner, data_dir):
    yield runner.crawl(XMLParser)

    with open(data_dir + '/meps.csv') as f:
        csv_data = csv.reader(f)
        for counter, line in enumerate(csv_data):
            full_name, id = line
            dir_name = f'{data_dir}/{full_name} - {id}'
            url = BASE_URL + id
            yield runner.crawl(MEPSCrawler, url=url, dir_name=dir_name)
            if counter == 0:
                break

    reactor.stop()


def main():
    project_settings = Settings(get_project_settings())
    runner = CrawlerRunner(settings=project_settings)
    crawl(runner, project_settings.get('DATA_DIR'))
    reactor.run()


if __name__ == '__main__':
    main()

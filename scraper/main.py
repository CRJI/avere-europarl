#!/usr/bin/python3

from scrapy.crawler import CrawlerRunner
from scraper.spiders.meps import XMLParser, MEPSCrawler
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
from twisted.internet import reactor, defer
from scrapy import signals

import csv
import os

BASE_URL = 'https://www.europarl.europa.eu/meps/en/'
COUNT_DECLARATIONS = 0


def do_count_decls(spider):
    if spider.has_declaration:
        global COUNT_DECLARATIONS
        COUNT_DECLARATIONS = COUNT_DECLARATIONS + 1


@defer.inlineCallbacks
def crawl(runner, data_dir):
    # if data directory does not exit create it
    if os.path.isdir(data_dir) is False:
        os.mkdir(data_dir)

    yield runner.crawl(XMLParser)

    with open(data_dir + '/meps.csv') as f:
        csv_data = csv.reader(f)
        for counter, line in enumerate(csv_data):
            full_name, id = line
            dir_name = f'{data_dir}/{full_name} - {id}'
            url = BASE_URL + id

            crawler_object = runner.create_crawler(MEPSCrawler)
            crawler_object.signals.connect(do_count_decls,
                                           signals.spider_closed)

            yield runner.crawl(crawler_object, url=url, dir_name=dir_name)

            if counter >= 2:
                break

        print(f'Number of MEPs: {counter+1}')
        print(f'MEPs with declarations: {COUNT_DECLARATIONS}')

    reactor.stop()


def main():
    project_settings = Settings(get_project_settings())
    runner = CrawlerRunner(settings=project_settings)
    crawl(runner, project_settings.get('DATA_DIR'))
    reactor.run()


if __name__ == '__main__':
    main()

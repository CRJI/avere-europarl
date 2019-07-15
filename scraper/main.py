#!/usr/bin/env python3

from scrapy.crawler import CrawlerRunner
from scraper.spiders.meps import XMLParser, MEPSCrawler
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
from twisted.internet import reactor, defer
from scrapy import signals

import argparse
import csv
import os

BASE_URL = 'https://www.europarl.europa.eu/meps/en/'
count_declarations = 0
count_meps = 0


def update_stats(spider):
    global count_meps
    count_meps = count_meps + 1

    if spider.has_declaration:
        global count_declarations
        count_declarations = count_declarations + 1


@defer.inlineCallbacks
def crawl(runner, data_dir):
    yield runner.crawl(XMLParser)

    with open(os.path.join(data_dir, 'meps.csv')) as f:
        csv_data = csv.reader(f)
        for line in csv_data:
            full_name, id = line
            dir_name = f'{data_dir}/{full_name} - {id}'
            url = BASE_URL + id

            crawler_object = runner.create_crawler(MEPSCrawler)
            crawler_object.signals.connect(update_stats,
                                           signals.spider_closed)

            yield runner.crawl(crawler_object, url=url, dir_name=dir_name)

    reactor.stop()


@defer.inlineCallbacks
def crawl_id(runner, data_dir, id):
    crawler_object = runner.create_crawler(MEPSCrawler)
    crawler_object.signals.connect(update_stats, signals.spider_closed)

    dir_name = f'{data_dir}/TEST - {id}'
    url = BASE_URL + id

    yield runner.crawl(crawler_object, url=url, dir_name=dir_name)

    reactor.stop()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', nargs=1, help='MEP id')
    args = parser.parse_args()

    os.environ['SCRAPY_SETTINGS_MODULE'] = 'scraper.settings'
    project_settings = Settings(get_project_settings())
    runner = CrawlerRunner(settings=project_settings)

    data_dir = project_settings.get('DATA_DIR')
    os.makedirs(data_dir, exist_ok=True)

    if args.id is None:
        crawl(runner, data_dir)
    else:
        crawl_id(runner, data_dir, args.id[0])

    reactor.run()

    print(f'Number of MEPs: {count_meps}')
    print(f'MEPs with declarations: {count_declarations}')


if __name__ == '__main__':
    main()

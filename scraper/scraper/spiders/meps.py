from scrapy.spiders import XMLFeedSpider
from scraper.items import MEP
import scrapy

import os


class XMLParser(XMLFeedSpider):
    name = 'mep_xml'
    start_urls = ['https://www.europarl.europa.eu/meps/en/directory/xml']
    iterator = 'iternodes'
    itertag = 'mep'
    c = 0

    def parse_node(self, response, node):
        id = node.xpath('id/text()').get()
        full_name = node.xpath('fullName/text()').get()

        return MEP(id=id, full_name=full_name)


class MEPSCrawler(scrapy.Spider):
    name = 'mep'
    base_url = 'https://www.europarl.europa.eu'

    def start_requests(self):
        os.mkdir(self.dir_name)
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        # get the table of contents on the left side and extract all links
        table = response.xpath(('//aside[@class="ep_gridcolumn '
                                'ep-layout_tableofcontent"]'))
        links = [self.base_url + x for x in table.xpath('.//a/@href').getall()
                 if x.startswith('/meps/')]

        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_page)

    def parse_page(self, response):
        print(response.url)
        pass

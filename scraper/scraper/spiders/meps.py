from scrapy.spiders import XMLFeedSpider
from scraper.items import MEP
import scrapy


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

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        print(response.body)

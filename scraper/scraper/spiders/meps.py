from scrapy.spiders import XMLFeedSpider
from scraper.items import MEP
import scrapy

import os


class XMLParser(XMLFeedSpider):
    name = 'mep_xml'
    start_urls = ['https://www.europarl.europa.eu/meps/en/directory/xml']
    iterator = 'iternodes'
    itertag = 'mep'

    def parse_node(self, response, node):
        id = node.xpath('id/text()').get()
        full_name = node.xpath('fullName/text()').get()

        return MEP(id=id, full_name=full_name)


class MEPSCrawler(scrapy.Spider):
    name = 'mep'
    base_url = 'https://www.europarl.europa.eu'

    def start_requests(self):
        if os.path.isdir(self.dir_name) is False:
            os.mkdir(self.dir_name)
        yield scrapy.Request(url=self.url, callback=self.parse_table)

    def parse_table(self, response):
        # get the table of contents on the left side and extract all links
        table = response.xpath(('//aside[@class="ep_gridcolumn '
                                'ep-layout_tableofcontent"]'))
        links = [self.base_url + x for x in table.xpath('.//a/@href').getall()
                 if x.startswith('/meps/')]

        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_page,
                                 dont_filter=True)

    def parse_page(self, response):
        page_content = response.xpath('//div[@class="ep_gridcolumn"]')
        title = page_content.xpath('.//span[@class="ep_name"]//text()').get()

        with open(f'{self.dir_name}/{title}.html', 'w') as f:
            f.write(page_content.get())

        declaration = page_content.xpath('.//span[@class="ep_name" '
                                         'and text()= "Declarations"]')

        # if in declaration section download all files
        if declaration.get():
            docs_section = declaration.xpath(('.//..//..//..//..//..//..//..//'
                                              '..//following-sibling::*'))
            docs = docs_section.xpath('.//a[@target="_blank" and '
                                      'contains(@title, "document")]'
                                      '//@href').getall()
            docs = list(set(docs))  # remove duplicates
            for doc in docs:
                yield scrapy.Request(url=doc, callback=self.save_file)

    def save_file(self, response):
        path = response.url.split('/')[-1]

        with open(f'{self.dir_name}/{path}', 'wb') as f:
            f.write(response.body)

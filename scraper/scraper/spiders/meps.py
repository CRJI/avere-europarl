from scrapy.spiders import XMLFeedSpider
from scraper.items import MEP
from bs4 import BeautifulSoup
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
    has_declaration = 0

    def start_requests(self):
        self.logger.info(f"Crawling MEP: {self.dir_name.split('/')[-1]}!")

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
        self.logger.info(f"Crawling page: {response.url}")

        page_content = response.xpath('//div[@class="ep_gridcolumn"]')
        title = page_content.xpath('.//span[@class="ep_name"]//text()').get()

        with open(f'{self.dir_name}/{title}.txt', 'w') as f:
            f.write(f'ORIGINAL URL: {response.url}\n\n\n')
            soup = BeautifulSoup(page_content.get(), 'html.parser')
            f.write("\n".join([ll.rstrip()
                    for ll in soup.get_text().splitlines() if ll.strip()]))

        decl_as_title = ('.//div[@class="ep_gridrow ep-o_product"]//div//div//'
                         'div//h1//div//div//span[text()="Declarations"]')
        decl_as_section = ('.//div[@class="ep_gridrow ep-o_product"]//div//div'
                           '//div//h2//div//div//span[text()="Declarations"]')
        declaration = page_content.xpath((f'{decl_as_title} '
                                          f'| {decl_as_section}'))

        # if in declaration section download all files
        if declaration.get():
            self.has_declaration = 1
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

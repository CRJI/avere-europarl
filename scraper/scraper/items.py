import scrapy


class MEP(scrapy.Item):
    full_name = scrapy.Field()
    id = scrapy.Field()



class ScraperPipeline(object):
    csv = ''

    def process_item(self, item, spider):
        if spider.name == 'mep_xml':
            self.csv += '{},{}\n'.format(item['full_name'], item['id'])
        return None

    def close_spider(self, spider):
        if spider.name == 'mep_xml':
            with open('links.csv', 'w') as f:
                f.write(self.csv)

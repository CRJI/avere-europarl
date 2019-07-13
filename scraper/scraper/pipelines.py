from scrapy.utils.project import get_project_settings
import csv


class SaveMepsCSV(object):
    meps = []

    def process_item(self, item, spider):
        if spider.name == 'mep_xml':
            self.meps.append((item['full_name'], item['id']))
        return None

    def close_spider(self, spider):
        if spider.name == 'mep_xml':
            dir_name = get_project_settings().get('DATA_DIR')
            with open(dir_name + '/meps.csv', 'w') as f:
                csv_file = csv.writer(f)
                csv_file.writerows(self.meps)

from scrapy.utils.project import get_project_settings
import csv
import os


class SaveMepsCSV(object):
    meps = []

    def process_item(self, item, spider):
        if spider.name != 'mep_xml':
            return

        self.meps.append((item['full_name'], item['id']))

    def close_spider(self, spider):
        if spider.name != 'mep_xml':
            return

        dir_name = get_project_settings().get('DATA_DIR')
        with open(os.path.join(dir_name, 'meps.csv'), 'w') as f:
            csv_file = csv.writer(f)
            csv_file.writerows(self.meps)

from scrapy.utils.project import get_project_settings

import logging
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
        filename = os.path.join(dir_name, 'meps.csv')
        with open(filename, 'w') as f:
            csv_file = csv.writer(f)
            csv_file.writerows(self.meps)

        logging.info(f"Xml saved as csv in {filename}!")

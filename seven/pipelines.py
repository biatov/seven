# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
import csv


class SevenPipeline(object):
    def __init__(self):
        self.date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.file = csv.writer(open('ry7_ru_%s.csv' % self.date, 'w'), quoting=csv.QUOTE_MINIMAL)
        self.file.writerow(['Для кого', 'Наименование', 'Тип/объем в милилитрах', 'Фото', 'Описание', 'Фильтры'])

    def process_item(self, item, spider):
        self.file.writerow([item['for_whom'], item['title'], item['value'], item['image_urls'], item['description'],
                            item['filters']])
        return item

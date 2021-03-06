# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SevenItem(scrapy.Item):
    for_whom = scrapy.Field()
    title = scrapy.Field()
    value = scrapy.Field()
    images = scrapy.Field()
    image_urls = scrapy.Field()
    photos = scrapy.Field()
    description = scrapy.Field()
    filters = scrapy.Field()

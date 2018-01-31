import scrapy
from scrapy.exceptions import CloseSpider
from ..items import SevenItem

import re


class Catalog(scrapy.Spider):
    name = 'catalog'
    allowed_domains = ['ry7.ru']
    start_urls = ['https://www.ry7.ru/']

    def parse(self, response):
        trading_xpath = '//li[@class="top1"]/a/@href'
        trading_urls = response.xpath(trading_xpath).extract()
        if trading_urls:
            for url in trading_urls:
                yield scrapy.Request(response.urljoin(url), callback=self.parse_trading_house)


    def parse_trading_house(self, response):
        products_xpath = '//a[@class="brnnew"]/@href'
        products_urls = response.xpath(products_xpath).extract()
        if products_urls:
            for url in products_urls:
                yield scrapy.Request(response.urljoin(url), callback=self.parse_product)

    def parse_product(self, response):
        product = SevenItem()
        no_data = ''

        def find_element(xpath_value, array=False):
            if array:
                element = list(filter(None, map(lambda i: i.strip(), response.xpath(xpath_value).extract())))
            else:
                try:
                    element = response.xpath(xpath_value).extract_first().strip()
                except AttributeError:
                    element = no_data
            return element

        def for_(whom):
            if whom[-2:] in 'ая':
                return ''.join([whom[:-2], 'ий'])
            return whom

        first_filter = find_element('//b[contains(text(), "аромат")]/text()')
        try:
            product['for_whom'] = for_(first_filter.split()[0].lower())
        except (AttributeError, IndexError, TypeError):
            product['for_whom'] = no_data

        product['title'] = find_element('//h1/text()')
        product['value'] = ', '.join(find_element(
            '//span[contains(@onmouseover, "код товара")]'
            '/parent::td/following-sibling::td[@class="title_mini" and @width="300"]'
            '/text()',
            array=True
        ))
        product['image'] = ', '.join(
            map(
                lambda i: i if 'http' in i else ''.join(
                    [
                        self.start_urls[0],
                        i[1:]
                    ]
                ),
                find_element('//img[@onclick="setBigImage(this)"]/@src', array=True)
            )
        )
        try:
            description = re.sub('<[^>]*>', '', find_element('//p[@itemprop="description"]'))
            description = re.sub('\s+', ' ', description)[10:]
        except AttributeError:
            description = no_data
        product['description'] = description

        filters = find_element('//b[contains(text(), "аромат")]/parent::span/parent::td/text()', array=True)
        filters = list(map(lambda i: re.sub('(\(\d*\))*', '', i).strip(), filters))
        filters.insert(0, first_filter)
        product['filters'] = ', '.join(filters)
        yield product

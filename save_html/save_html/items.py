# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SaveHtmlItem(scrapy.Item):
    url = scrapy.Field()
    body = scrapy.Field()
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LiepinwangItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    company = scrapy.Field()
    salary = scrapy.Field()
    city = scrapy.Field()
    edu = scrapy.Field()
    experience = scrapy.Field()
    desc = scrapy.Field()

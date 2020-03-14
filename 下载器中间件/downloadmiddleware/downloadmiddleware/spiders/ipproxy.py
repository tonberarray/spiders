# -*- coding: utf-8 -*-
import scrapy


class IpproxySpider(scrapy.Spider):
    name = 'ipproxy'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/ip']

    def parse(self, response):
        print('+'*30)
        print(response.text)
        print('+'*30)

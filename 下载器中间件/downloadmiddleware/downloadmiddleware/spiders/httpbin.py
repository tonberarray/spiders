# -*- coding: utf-8 -*-
import scrapy


class HttpbinSpider(scrapy.Spider):
    name = 'httpbin'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/user-agent']

    def parse(self, response):
        print('+'*30)
        print(response.text)
        print('+'*30)
        yield scrapy.Request(self.start_urls[0],dont_filter=True)
        # dont_filter=True,scrapy 有自动去重的功能，当一个网络请求已经执行过，
        # scrapy就会自动过滤掉，不再执行，参数dont_filter=True则表示不再过滤
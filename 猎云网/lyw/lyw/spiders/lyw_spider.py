# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import LywItem

class LywSpiderSpider(CrawlSpider):
    name = 'lyw_spider'
    allowed_domains = ['lieyunwang.com']
    start_urls = ['https://www.lieyunwang.com/latest/p1.html']

    rules = (
        Rule(LinkExtractor(allow=r'/latest/p\d+\.html'), follow=True),
        Rule(LinkExtractor(allow=r'/archives/\d+'), callback='parse_detail', follow=False),
    )

    def parse_detail(self, response):
        title_list = response.xpath("//h1[@class='lyw-article-title']/text()").getall()
        title = ''.join(title_list).strip()
        pub_time = response.xpath("//h1[@class='lyw-article-title']/span/text()").get()
        author = response.xpath("//a[contains(@class,'author-name')]/text()").get()
        content = response.xpath("//div[@id='main-text-id']").get()
        origin = response.url 
        item = LywItem(title=title,pub_time=pub_time,author=author,content=content,
        	origin=origin)
        yield item
        # 也可以是 return item， CrawlSpider中有自己迭代的方法
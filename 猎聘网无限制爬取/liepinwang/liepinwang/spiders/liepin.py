# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import LiepinwangItem

class LiepinSpider(CrawlSpider):
    name = 'liepin'
    allowed_domains = ['liepin.com']
    start_urls = ['https://www.liepin.com/zhaopin/?key=python']
# https://www.liepin.com/job/1925659053.shtml
    rules = (
        Rule(LinkExtractor(allow=r'/zhaopin/.+curPage=\d+', restrict_xpaths=["//div[@class='pagerbar']//a"]), follow=True),
        Rule(LinkExtractor(allow=r'https.+/job/\d+\.shtml.*', restrict_xpaths=["//ul[@class='sojob-list']//a"]), callback='parse_job', follow=False),
    )

    def parse_job(self, response):
        # title = response.xpath("//div[@class='title-info']/h1/text()").get()
        # company = response.xpath("//div[@class='title-info']/h3/a/text()").get()
        # pay = response.xpath("//div[@class='job-title-left']/p/text()").get().strip()
        # city =  response.xpath("//div[@class='job-title-left']/p[@class='basic-infor']//a/text()").get()
        # edu =  response.xpath("//div[@class='job-qualifications']/span[1]/text()").get()
        # experience =  response.xpath("//div[@class='job-qualifications']/span[2]/text()").get()
        # desc_list =  response.xpath("//div[@class='content content-word']/text()").getall()
        # desc = ''.join(desc_list).strip()

        title = response.css(".title-info h1::text").get()
        company = response.css(".title-info h3 a::text").get()
        salary = response.css(".job-title-left p::text").get().strip() 
        city = response.css(".basic-infor a::text").get()
        edu = response.css(".job-qualifications span:nth-child(1)::text").get()
        experience = response.css(".job-qualifications span:nth-child(2)::text").get()
        desc_list = response.css(".content-word::text").getall()
        desc = "".join(desc_list).strip()
        item = LiepinwangItem(title=title,company=company,salary=salary,city=city,
            edu=edu,experience=experience,desc=desc)
        yield item

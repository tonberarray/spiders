# -*- coding: utf-8 -*-
import scrapy
from ..items import LjItem
import json
import re


class LjSpiderSpider(scrapy.Spider):
    name = 'LJ_spider'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://www.lianjia.com/city/']

    def parse(self, response):
    	# 解析获得每个城市链接
        city_tags = response.css(".city_list_ul li a")
        for city_tag in city_tags:
        	city_name = city_tag.css("::text").get()
        	city_url = city_tag.css("::attr(href)").get()
        	item = LjItem(city=city_name)
        	yield scrapy.Request(city_url + "ershoufang/",
        		callback=self.parse_region_list,meta={"item":item})

    def parse_region_list(self, response):
    	# 解析对应行政区域链接
      	item = response.meta.get("item") 
      	region_tags = response.css("div[data-role='ershoufang'] a")
      	for region_tag in region_tags:
      		item['region'] = region_tag.css("::text").get()
      		region_url = region_tag.css("::attr(href)").get()
      		yield scrapy.Request(response.urljoin(region_url),
      			callback=self.parse_house_pages,meta={"item":item})

    def parse_house_pages(self, response):
    	# 实现翻页
    	page_data = response.css("div[comp-module='page']::attr(page-data)").get()
    	totalPage = json.loads(page_data)['totalPage']
    	for x in range(1,totalPage):
    		yield scrapy.Request(response.url+"pg"+str(x),
    			callback=self.parse_house_list,
    			meta={"item":response.meta.get("item")})

    def parse_house_list(self, response):
    	# 解析房源列表
    	detail_urls = response.css(".sellListContent li>a::attr(href)").getall()
    	for detail_url in detail_urls:
    		# 对提取的过滤网页进行,剔除动态未加载
    		result = re.search(r"/ershoufang/\d+\.html",detail_url)
    		if result:
    			yield scrapy.Request(detail_url,
    				callback=self.parse_detail_page,
    				meta={"item":response.meta.get("item")})

    def parse_detail_page(self, response):
    	# 解析房源详情页
    	item = response.meta.get("item")	
    	item['title'] = response.css(".title h1::text").get()
    	item['total_price']	= response.css(".price .total::text").get() + "万元"
    	item['unit_price'] = response.css(".price .unitPriceValue::text").get() + "元/平米"
    	item['house_type'] = response.css(".content ul li:nth-child(1)::text").get()
    	item['orientation'] = response.css(".content ul li:nth-child(7)::text").get()
    	item['full_area'] =  response.css(".content ul li:nth-child(3)::text").get()
    	item['inside_area'] = response.css(".content ul li:nth-child(5)::text").get()
    	item['years'] = response.css(".area .subInfo::text").get()
    	yield item

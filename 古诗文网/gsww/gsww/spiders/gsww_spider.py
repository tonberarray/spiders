# -*- coding: utf-8 -*-
import scrapy
from ..items import GswwItem

class GswwSpiderSpider(scrapy.Spider):
    name = 'gsww_spider'
    allowed_domains = ['gushiwen.org']
    start_urls = ['https://www.gushiwen.org/default_1.aspx']

    def myprint(self, value):
        print('*'*30)
        print(value)

    def parse(self, response):
        # self.myprint(type(response))  # <class 'scrapy.http.response.html.HtmlResponse'>
        gsw_divs = response.xpath("//div[@class='left']/div[@class='sons']/div[@class='cont']")
        # self.myprint(type(gsw_divs)) # <class 'scrapy.selector.unified.SelectorList'>
        # response.xpath请求回来的数据都是SelectorList对象，里面存储的都是Selector对象
        # SelectorList对象形如[<Selector xpath='.//b/text()' data='点绛唇·春眺'>]
        # SelectorList.getall()：可以直接获取xpath中指定的值。
        # SelectorList.get()：可以直接获取xpath匹配的第一个值。
        for gsw_div in gsw_divs:
            title = gsw_div.xpath(".//b/text()").get()
            source = gsw_div.xpath(".//p[@class='source']/a/text()").getall()
            dynasty = source[0]
            author = source[1]
            content_list = gsw_div.xpath(".//div[@class='contson']//text()").getall()
            content = "".join(content_list).strip()
            item = GswwItem(title=title,dynasty=dynasty,author=author,content=content)
            yield item 
            # 使用yield迭代器，在pipeline将数据写入时避免重复和异常 
        
        # 获取下一页的标签，将下一页的请求返回给调度器以分配执行请求下一页爬取
        next_href = response.xpath("//a[@id='amore']/@href").get() # href="/default_2.aspx"
        # 执行一个判断，如果没有下一页，则终止请求
        if next_href:   
            # response.urljoin()将domain进行拼接获得下一页的网址
            next_url = response.urljoin(next_href)
            request = scrapy.Request(next_url)
            yield request
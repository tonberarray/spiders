# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from json import dumps


class LiepinwangPipeline(object):
    def open_spider(self,spider):
        self.fp = open("jobs.txt","w",encoding='utf-8')

    def process_item(self, item, spider):
        self.fp.write(dumps(dict(item),ensure_ascii=False) + "\n")
        return item

    def close_spider(self,spider):
        self.fp.close()
        
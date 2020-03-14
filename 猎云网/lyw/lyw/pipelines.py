# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# 异步存储操作需要调用twisted模块里面的adbapi
from twisted.enterprise import adbapi

class LywPipeline(object):
    def __init__(self,mysql_config):
        self.dbconn = adbapi.ConnectionPool(
            mysql_config['DRIVER'],
            host = mysql_config['HOST'],
            port = mysql_config['PORT'],
            user = mysql_config['USER'],
            password = mysql_config['PASSWORD'],
            db = mysql_config['DATABASE'],
            charset = 'utf8'
            )

    @classmethod
    def from_crawler(cls, crawler):
        # 只要重写了from_crawler方法，那么以后创建对象的时候，就会调用这个方法来获取pipline对象
        mysql_config = crawler.settings["MYSQL_CONFIG"]
        return cls(mysql_config)

    def process_item(self, item, spider):
        result = self.dbconn.runInteraction(self.insert_item,item)
        result.addErrback(self.error_print)
        return item

    def insert_item(self,cursor,item):
        sql = "insert into articles(title,author,pub_time,content,origin) values(%s,%s,%s,%s,%s)" 
        values = (item['title'],item['author'],item['pub_time'],item['content'],item['origin'])
        cursor.execute(sql,values)

    def error_print(self,failure):
        print('+'*30)
        print(failure)   
        print('+'*30)

    def close_spider(self,spider):
        self.dbconn.close()   
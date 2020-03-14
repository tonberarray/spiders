# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
from scrapy import signals
from fake_useragent import UserAgent
import base64


class UserAgentDownloaderMiddleware(object):
    def process_request(self, request,spider):
        ua = UserAgent()
        request.headers['User-Agent'] = ua.random


class IpProxyDownloaderMiddleware(object):
    # 普通代理
    PROXIES = [{"ip":"124.113.192.168","port":4231,"expire_time":"2019-05-09 22:58:55"},{"ip":"117.57.35.70","port":4273,"expire_time":"2019-05-09 22:58:55"}]
    def process_request(self, request,spider):
        proxy = random.choice(self.PROXIES)
        # http://124.113.192.168:4231
        proxy_url = "http://" + proxy["ip"] + ":" + str(proxy["port"])
        request.meta['proxy'] = proxy_url
 
       
# class IpProxyDownloaderMiddleware(object):
#     # 专享代理
#     def process_request(self, request,spider):
#         proxy = '121.199.6.124:16816'
#         user_password = "970138074:rcdj35xx"
#         request.meta['proxy'] = proxy
#         b64_user_password = base64.b64encode(user_password.encode('utf-8'))
#         request.headers['Proxy-Authorization'] = "Basic" + b64_user_password.decode('utf-8')
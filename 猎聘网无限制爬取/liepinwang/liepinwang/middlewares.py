# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import requests
from .models import ProxyModel
from time import sleep
import threading


class ProxyDownloaderMiddleware(object):
	def __init__(self):
		super(ProxyDownloaderMiddleware,self).__init__()
		self.current_proxy = None
		self.update_proxy_url = "http://d.jghttp.golangapi.com/getip?num=1&type=2&pro=&city=0&yys=0&port=11&time=1&ts=1&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions="
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
		}
		self.update_proxy()
		self.lock = threading.Lock()
		# 创建一个线程，专门用来管理IP代理更新
		# 管理方式：当前IP代理使用超过一分钟或者被拉黑，多线程就更换代理IP
		thread = threading.Thread(target=self.update_proxy_in_thread)
		thread.start()

	def process_request(self, request, spider):
		# 更换代理，是在请求之前更换，也就是在这个函数中更换的
		request.meta["proxy"] = self.current_proxy.proxy_url
		return None

	def process_response(self, request, response, spider):
		# 响应中通过判断状态码来确定是否需要更换代理
		if response.status != 200:
			# 标记代理的标记位，以提示需要更换代理
			self.lock.acquire()
			self.current_proxy.is_blacked = True
			self.lock.release()
			# 若当前请求没有正确响应，则需要将请求返回，以重新请求爬取信息
			return request
		# 如果请求正常响应，一定要将响应返回，否则在爬虫中获取不到信息	
		return response

	def update_proxy(self):
		resp = requests.get(self.update_proxy_url,headers=self.headers)
		self.current_proxy = ProxyModel(resp.json())
		print("更新了代理IP为: %s" %(self.current_proxy.proxy_url))

	def update_proxy_in_thread(self):
		# 当前IP代理使用超过一分钟或者被拉黑，多线程就更换代理IP
		count = 0 
		while True:
			sleep(10)
			if count >= 6 or self.current_proxy.is_blacked:
				self.update_proxy()
				count = 0
			else:
				count += 1
				print("count + 1 = %d" %count)
	

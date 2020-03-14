# coding = utf-8
from datetime import datetime
from datetime import timedelta


# {'code': 0, 'data': [{'expire_time': '2020-02-12 23:30:41', 'ip': '182.86.5.222', 'port': 45761}], 'msg': '0', 'success': True}
class ProxyModel(object):
	"""docstring for ProxyModel"""
	def __init__(self, proxy_dict):
		proxy = proxy_dict["data"][0]
		self.proxy_url = "https://" + proxy["ip"] + ":" + str(proxy["port"])
		self.expire_time = datetime.strptime(proxy['expire_time'],"%Y-%m-%d %H:%M:%S")
		self.is_blacked = False # IP是否被加入黑名单

	@property
	def is_expiring(self):
		# 当前时间如果比过期时间小五秒，视为将过期，需更新代理
		if (self.expire_time - datetime.now()) <= timedelta(seconds=5):
			return True
		else:
			return False
		 

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException,ElementNotVisibleException,ElementNotInteractableException
import time
import csv

# 设置代理IP
# options = webdriver.ChromeOptions()
# options.add_arguement("--proxy-server=http://183.166.110.166:9999")
# driver = webdriver.Chrome(executable_path=r"E:\chromedriver.exe",chrome_options=options)


"""
将driver放在外面作为全局变量。因为TrainSpider的实例
是放在main函数中运行的，main函数中代码执行完后，
其使用的内存会立即释放掉，TrainSpider里面的变量
也就没法继续维持，如果driver放在TrainSpider中，
浏览器会在main函数执行完后立刻退出。 
"""
driver = webdriver.Chrome(executable_path=r"E:\chromedriver.exe")

class TrainSpider(object):
	# 登录页
	login_url = "https://kyfw.12306.cn/otn/resources/login.html"
	# 登录后个人页面
	personal_url = "https://kyfw.12306.cn/otn/view/index.html"
	# 余票查询页
	left_tickets_url = "https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc"
	# 确认乘客和座次页面
	confirm_passenger_url = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"

	def __init__(self, from_station,to_station,train_date,trains,passengers):
		"""
		:param from_station: 出发地站点名称
        :param to_station: 目的地站点名称
        :param train_date: 出发日期
        :param trains: 需要为一个字典，可以为多个车次。示例如：{"G594":['M','O'],"D2262":['M','O']}
        :param passengers: 乘客姓名
		"""
		self.from_station = from_station
		self.to_station = to_station
		self.train_date = train_date
		self.trains = trains
		self.passengers = passengers
		self.station_codes = {}
		self.current_number = None # 当前车次
		self.init_station_codes()

	def init_station_codes(self):
		# 初始化车站编码
		with open("stations.csv", "r",encoding="utf-8") as fp:
			reader = csv.DictReader(fp)
			for line in reader:
				name = line["name"]
				code = line["code"]
				self.station_codes[name] = code

	def login(self):
		driver.get(self.login_url)
		# 确定登录成功
		WebDriverWait(driver,1000).until(
		EC.url_contains(self.personal_url)
			)
		print("登录成功！")
		pass	

	def search_left_tickets(self):
		driver.get(self.left_tickets_url)
		# 起始站设置
		from_code = self.station_codes[self.from_station]
		from_input = driver.find_element_by_id("fromStation")
		driver.execute_script("arguments[0].value='%s'"%(from_code),from_input)
		# 终点站设置
		to_code = self.station_codes[self.to_station]
		to_input = driver.find_element_by_id("toStation")
		driver.execute_script("arguments[0].value='%s'"%(to_code),to_input)
		# 日期设置
		train_date_input = driver.find_element_by_id("train_date")
		driver.execute_script("arguments[0].value='%s'"%(self.train_date),train_date_input)
		query_btn = driver.find_element_by_id("query_ticket")
		# 死循环，没有票就一直执行查询命令,直到成功抢到票
		while True:		
			query_btn.click()

			# 余票解析
			# 等待查询的车次出现
			WebDriverWait(driver,100).until(
				EC.presence_of_element_located((By.XPATH,"//tbody[@id='queryLeftTable']/tr"))
				)
			train_trs = driver.find_elements_by_xpath("//tbody[@id='queryLeftTable']/tr[not(@datatran)]")
			# 查找车次
			is_searched = False # 查找到余票的标志
			for train_tr in train_trs:
				train_info = train_tr.text.replace('\n', ' ').split(' ')
				orderable = train_info[-1]
				if orderable != "预订":
					continue
				number = train_info[0] # 车次
				if number in self.trains:
					for seat_type in self.trains[number]:
						# 二等座
						if seat_type == 'O':
							count = train_info[9]
							if count.isdigit() or count == "有":
								is_searched = True
								break
						# 一等座		
						elif seat_type == 'M':
							count = train_info[8]
							if count.isdigit() or count == "有":
								is_searched = True
								break
				# 如果刷到票，提交订单，退出循环				
				if is_searched:
					self.current_number = number
					order_btn = train_tr.find_element_by_xpath(".//a[@class='btn72']")
					order_btn.click()
					return

	def confirm_passengers(self):

		# 等待跳转到乘客信息确认页面
		WebDriverWait(driver,1000).until(
			EC.url_contains(self.confirm_passenger_url)
			)
		# 等待乘客信息元素加载完毕
		WebDriverWait(driver,1000).until(
			EC.presence_of_element_located((By.XPATH,"//ul[@id='normal_passenger_id']/li"))
			)		
		# 将需要购票的乘客选中。
		passenger_labels = driver.find_elements_by_xpath("//ul[@id='normal_passenger_id']/li/label")
		for passenger_label in passenger_labels:
			if passenger_label.text in self.passengers:
				passenger_label.click()
		# 等待座次元素加载完毕
		WebDriverWait(driver,1000).until(
			EC.presence_of_element_located((By.XPATH,"//select[@id='seatType_1']/option"))
			)
		# 选择座次
		seat_select = Select(driver.find_element_by_id("seatType_1"))
		for seat_type in self.trains[self.current_number]:
			try:
				seat_select.select_by_value(seat_type)
			except NoSuchElementException:
				continue
			else:
				break

		# 等待提交订单按钮可用,然后点击提交
		WebDriverWait(driver,1000).until(
			EC.element_to_be_clickable((By.ID,"submitOrder_id"))
			)
		submit_order_btn = driver.find_element_by_id("submitOrder_id")
		submit_order_btn.click()
		# 等待核对订单信息的对话框弹出加载
		WebDriverWait(driver,1000).until(
			EC.presence_of_element_located((By.CLASS_NAME,"dhtmlx_window_active"))
			)
		# 确认订单，提交确认
		WebDriverWait(driver,1000).until(
			EC.element_to_be_clickable((By.ID,"qr_submit_id"))
			)
		confirm_btn = driver.find_element_by_id("qr_submit_id")
		while confirm_btn:
			try:
				confirm_btn.click()
				confirm_btn = driver.find_element_by_id("qr_submit_id")
			except (ElementNotVisibleException, ElementNotInteractableException) as exce:
				break
		print("恭喜！！！您已成功抢到【%s】车次的车票，请在30分钟内完成付款！"%(self.current_number))
		time.sleep(900)

	def run(self):
		# 1. 登录
		self.login()
		# 2.余票查询
		self.search_left_tickets()
		# 3.确认乘客和座次
		self.confirm_passengers()

		pass

def main():
	# 9：商务座，M：一等座，O：二等座，3：硬卧，4：软卧，1：硬座
	spider = TrainSpider("杭州","武汉","2020-02-13",{"G594":['O','M'],"D2262":['O','M']},["唐白光"])
	spider.run()

if __name__ == '__main__':
	main()		
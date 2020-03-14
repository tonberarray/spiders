import requests

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}
# {"code":0,"data":[{"expire_time":"2020-02-12 23:22:18","ip":"182.105.201.13","port":45751}],"msg":"0","success":true}
update_proxy_url = "http://d.jghttp.golangapi.com/getip?num=1&type=2&pro=&city=0&yys=0&port=11&time=1&ts=1&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions="

response = requests.get(update_proxy_url,headers=headers)
result = response.json()
print(type(result)) # <class 'dict'>
print(result) # {'code': 0, 'data': [{'expire_time': '2020-02-12 23:30:41', 'ip': '182.86.5.222', 'port': 45761}], 'msg': '0', 'success': True}
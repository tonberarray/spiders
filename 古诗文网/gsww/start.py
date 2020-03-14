from scrapy import cmdline

# cmdline.execute("scrapy crawl gsww_spider".split(" "))
# 启动命令的另一种写法。
cmds = ["scrapy", "crawl", "gsww_spider"]
cmdline.execute(cmds)

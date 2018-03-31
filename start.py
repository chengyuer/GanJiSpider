from scrapy import cmdline

headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);"}

cmdline.execute(["scrapy","crawl","fuckganji"])

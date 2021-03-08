import scrapy 
import json 
import os
import os.path
import re
import time
import codecs
linkitem = []
listID = []
f2 = codecs.open("data.txt", "a", "utf-8")
class Demo(scrapy.Spider):
    name = "demo"
    allowed_domains = ["lazada.vn"]
    f = open("ID2.txt","r")
    line = f.readline()
    start_urls = []

    while line:
        url = "https://my.lazada.vn/pdp/review/getReviewList?itemId="+ line.strip()+ "&pageSize=20&filter=0&sort=0&pageNo="
        for i in range(40):
            tmp = url+str(i+6)
            start_urls.append(tmp)
        
        line = f.readline()
        
    def start_requests(self):
    
        for url in self.start_urls:
            time.sleep(2)
            yield scrapy.Request(url=url, callback=self.parse)
        # yield scrapy.Request(url=self.start_urls[1], callback=self.parse)
    def parse(self, response):
        data = json.loads(response.body)
        # print(response.body)
        s1 = u""
        for i in range(len(data["model"]["items"])):
            s1 = data["model"]["items"][i]["reviewContent"].replace('\n', ' ')
            s1 = s1.replace('\r', ' ')
            f2.write(str(data["model"]["items"][i]["rating"])+"   "+ s1+ "\n")

import scrapy 
import json 
import os
import os.path
import re
import time
import codecs
linkitem = []
listID = []
f2 = codecs.open("data_bag_final.txt", "a+", "utf-8")

class Get_comment_bag(scrapy.Spider):
    name = "demo1"
    allowed_domains = ["lazada.vn","my.lazada.vn"]
    f = open("ID3.txt","r")
    line = f.readline()
    start_urls = []

    while line:
        url1 = "https://my.lazada.vn/pdp/review/getReviewList?itemId="+ line.strip() + "&pageSize=20&filter=0&sort=0&pageNo=1"
        # for i in range(30) :
        #     tmp = url1 + str(i+1)
        #     start_urls.append(tmp)
        start_urls.append(url1)
        line = f.readline()
        
    def start_requests(self):
        for url in self.start_urls:
            time.sleep(1.8)
            yield scrapy.Request(url=url, callback=self.parse)
        # yield scrapy.Request(url=self.start_urls[1], callback=self.parse)
    def parse(self, response):
        data = json.loads(response.body)
        s1 = u""
        if data["model"]["items"] != None :
            for i in range(len(data["model"]["items"])):
                s1 = data["model"]["items"][i]["reviewContent"].replace('\n', ' ')
                s1 = s1.replace('\r', ' ')
                f2.write(str(data["model"]["items"][i]["rating"])+"   "+ s1+ "\n")
            url = response.url[:len(response.url)-1] + str(int(response.url[len(response.url)-1])+1)
            yield scrapy.Request(url=url, callback=self.parse)
        
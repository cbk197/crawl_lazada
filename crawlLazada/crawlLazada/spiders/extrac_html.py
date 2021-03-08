import scrapy 
import json 
import os
import os.path
import re
import time
import codecs
linkitem = []
listID = []
f = open("ID.txt","a+")

class Extrac_HTML(scrapy.Spider):
    name = "extract_html"
    allowed_domains = ["lazada.vn"]
    start_urls = ["https://www.lazada.vn/"]
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        select = "ul.lzd-site-menu-sub:nth-child(13)"
        for i in range(12):
            tem = select.replace("13", str(i+13))
            link = response.css(tem)
            tmp = link.xpath(".//li[@class=\"lzd-site-menu-sub-item\"]/a")
            for l in tmp:
                t = l.xpath("@href").extract_first().split("/")
                linkitem.append(t[3])
            
        index = 0
        for i in range(len(linkitem)):
            linkitem[i] = "https://www.lazada.vn/"+linkitem[i].strip()
            
        
        
        
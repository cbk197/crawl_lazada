import scrapy 
import json 
import os
import os.path
import re
import time
import codecs
from scrapy_splash import SplashRequest
linkitem = []
listID = []
f = open("ID2.txt","a+")
lua_script = """
function main(splash)
    local num_scrolls = 10
    local scroll_delay = 1.0
    local scroll_to = splash:jsfunc("window.scrollTo")
    local get_body_height = splash:jsfunc(
        "function() {return document.body.scrollHeight;}"
    )
    assert(splash:go(splash.args.url))
    splash:wait(splash.args.wait)
    for _ = 1, num_scrolls do
        scroll_to(0, get_body_height())
        splash:wait(scroll_delay)
    end
    return splash:html()
end
"""
script = """
function main(splash, args)
    splash.images_enabled = false
    splash.private_mode_enabled = false
    splash.request_body_enabled = true
    splash.html5_media_enabled = true
    splash.resource_timeout = 5
    splash:on_request(function(request)
        if first then
            request:set_timeout(15.0)
            first = false
        end
    end)
    splash:go(args.url)
    splash:wait(0.4)
    local scroll_to = splash:jsfunc("window.scrollTo")
    scroll_to(0, 1000)
    splash:wait(1)
    return {html = splash:html()}
    
end
"""

class CrawlLazada(scrapy.Spider):
    name = "lazada"
    allowed_domains = ["lazada.vn"]
    start_urls = ["https://www.lazada.vn/"]
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        select = "ul.lzd-site-menu-sub:nth-child(13)"
        fx = open("chuan.html","wb")
        fx.write(response.body)
        l = response.css('html body div#J_icms-5000454-1511536528265.mui-zebra-module div#J_LzdSiteNav.site-nav.J_NavScroll div.lzd-home-page-category div#J_icms-5000524-1511531104744.mui-zebra-module div.lzd-site-nav-menu div.lzd-site-menu-nav-container div.lzd-site-menu-nav-category div.lzd-site-menu-nav-menu.lzd-site-menu-show-category div#J_icms-5000514-1511529253108.mui-zebra-module div.lzd-site-nav-menu-dropdown ul.lzd-site-menu-root ul.lzd-site-menu-sub.Level_1_Category_No10 li.lzd-site-menu-sub-item a')

        # for i in range(12):
        #     tem = select.replace("13", str(i+13))
        #     link = response.css(tem)
        #     tmp = link.xpath(".//li[@class=\"lzd-site-menu-grand-item\"]/a")
            
        #     for l in tmp:
        #         t = l.xpath("@href").extract_first().split("/")
        #         linkitem.append(t)
        #         print(t)
            
        
        # for i in range(len(linkitem)):
        #     linkitem[i] = "https://www.lazada.vn/"+linkitem[i].strip()
        for l1 in l:
            t = l.xpath("@href")
            linkitem.append(t)
            print(t)
            
        
        # for i in range(len(linkitem)):
            # time.sleep(5)
            # yield SplashRequest(url= linkitem[i], endpoint='execute',
                                # args={'lua_source': lua_script}, callback = self.parseID )
            
        
        # yield scrapy.Request(url=linkitem[55], callback=self.parseID)
        
        

    def parseID(self, response):
        link = response.css("html body div#root div.c2P49E div.ant-row.c10-Cg div.ant-col-24 div.ant-row div.ant-col-20.ant-col-push-4.c1z9Ut div.c1_t2i div.c2prKC div.c3e8SH div.c5TXIP div.c2iYAv div.cRjKsc a")
        
        for l in link:
            x = re.findall("i[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]",l.xpath("@href").extract_first())
            if x[0] != []:
                x[0] = x[0][1:]
                f.write(x[0]+"\n") 
    
    
    def parseID1(self, response):
        data = json.loads(response.body)
        # f.write(str(data["mods"]["listItems"][0]["nid"]))
        # print(response.body)
        for i in range(len(data["mods"]["listItems"])):
            f.write(data["mods"]["listItems"][i]["nid"]+"\n")
        #     url1 = "https://my.lazada.vn/pdp/review/getReviewList?itemId="+ data["mods"]["listItems"][i]["nid"]+ "&pageSize=20&filter=0&sort=0&pageNo=1"
        #     url2 = "https://my.lazada.vn/pdp/review/getReviewList?itemId="+ data["mods"]["listItems"][i]["nid"]+ "&pageSize=20&filter=0&sort=0&pageNo=2"
        # yield scrapy.Request(url=url1, callback=self.parseID2)
        # yield scrapy.Request(url=url2, callback=self.parseID2)

    def parseID2(self, response):
        pass
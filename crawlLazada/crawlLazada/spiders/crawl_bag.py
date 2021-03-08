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
f = open("bag_ID.txt","a+")
lua_script = """
function main(splash)
    splash.images_enabled = false
    splash.private_mode_enabled = false
    local num_scrolls = 2
    local scroll_delay = 8
    local scroll_to = splash:jsfunc("window.scrollTo")
    local get_body_height = splash:jsfunc(
        "function() {return document.body.scrollHeight;}"
    )
    assert(splash:go(splash.args.url))
    splash:set_viewport_full()
    splash:wait(4)
    
    return splash:html()
end
"""
# for _ = 1, num_scrolls do
    #     scroll_to(0, get_body_height())
    #     splash:wait(scroll_delay)
    # end
    # element = splash:select('li.ant-pagination-item:nth-child(6)')
    # local bounds = element:bounds()
    # assert(element:mouse_click{x=bounds.width/3, y=bounds.height/3})
    # splash:wait(4)
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
    name = "list_bag"
    allowed_domains = ["lazada.vn"]
    start_urls = ["https://www.lazada.vn/tui-cho-nu/?spm=a2o4n.home.cate_10.5.1905e182nzY097"]
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url= url, endpoint='execute',
                                args={'lua_source': lua_script}, callback = self.parseID )

    
        

    def parseID(self, response):
        link = response.css("html body div#root div.c2P49E div.ant-row.c10-Cg div.ant-col-24 div.ant-row div.ant-col-20.ant-col-push-4.c1z9Ut div.c1_t2i div.c2prKC div.c3e8SH.c2mzns div.c5TXIP div.c2iYAv div.cRjKsc a")
        f.write(response.url)     
        f.write('\n')           
        for l in link:
            x = re.findall("i[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]",l.xpath("@href").extract_first())
            if x[0] != []:
                x[0] = x[0][1:]
                f.write(x[0]+"\n") 
        url = 'https://www.lazada.vn/tui-cho-nu/?page=2&spm=a2o4n.home.cate_10.5.1905e182nzY097'
        listLink = []
        listLink.append(url)
        for i in range(18):
            tmp = url.replace('page=2', 'page='+str(i+3))
            listLink.append(tmp)
        
        yield SplashRequest(url= url, endpoint='execute',
                            args={'lua_source': lua_script},headers={'Referer':'https://www.lazada.vn/tui-cho-nu/?spm=a2o4n.home.cate_10.5.1905e182nzY097'}, callback = self.parseID1 )

    

    def parseID1(self, response):
        link = response.css('html body div#root div.c2P49E div.ant-row.c10-Cg div.ant-col-24 div.ant-row div.ant-col-20.ant-col-push-4.c1z9Ut div.c1_t2i div.c2prKC div.c3e8SH.c2mzns div.c5TXIP div.c2iYAv div.cRjKsc a')
        f.write(response.url)     
        f.write('\n')   
        for l in link:
            x = re.findall("i[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]",l.xpath("@href").extract_first())
            if x[0] != []:
                x[0] = x[0][1:]
                f.write(x[0]+"\n") 
        url = response.url
        s= re.findall('page=\d+',url)
        num = re.findall('\d+',str(s[0]))
        tmp = int(num[0])
        tmp+=1 
        newpage  = 'page='+str(tmp)
        url = url.replace(s[0], newpage)
        yield SplashRequest(url= url, endpoint='execute',
                            args={'lua_source': lua_script}, callback = self.parseID1 )


        
from scrapy.spider import BaseSpider
from scrapy.http import FormRequest
from scrapy.selector import HtmlXPathSelector
import pymongo
from scrapy.shell import inspect_response
from scrapy.http import Request
from time import sleep
import re
# from selenium import webdriver
# from ..items import PluscrawlItem
from ..items import MyspaceItem

class MyspaceSpider(BaseSpider):

    name = 'myspace'

    #you can extent the list from multions_myspace
    # g_ = open('id_lists.dat', 'r')
    mongo = pymongo.Connection("10.1.1.111", 12345)["myspace"]["profiles"]
    start_urls = []
    # for e in g_:
    #     start_urls.append('https://myspace.com/'+e.strip()+'/connections/in')
    #     start_urls.append('https://myspace.com/'+e.strip()+'/connections/out')
    #
    method = 0
    """
    crawl seed profile
    """
    if method == 0:
        res = mongo.find()
        for item in res:
            start_urls.append('https://myspace.com/'+item["_id"]+'/connections/in')
            start_urls.append('https://myspace.com/'+item["_id"]+'/connections/out')
            # start_urls.append('http://www.flickr.com/people/' + item["_id"] + '/contacts/')

    """
    crawl all friends
    """
    if method == 1:
        seed_set = set()
        item_set = set()
        res = mongo.find()
        for item in res:
            seed_set.add(item["_id"])
            if "friend" in item:
                for f in item["friend"]:
                    item_set.add(f)
        for item in item_set - seed_set:
            start_urls.append('http://' + item + '.livejournal.com/profile')
            # start_urls.append('http://www.flickr.com/people/' + item + '/contacts/')
    print len(start_urls), "to crawl"

    def get_id(self, url):
        find_index = url.find("myspace.com/")
        if find_index >= 0:
            x = url[find_index:].split("/")
            print x[1]
            return x[1]
        return None

    def getFriends(self,hxs):
        friends = hxs.select('//div[@class="mediaSquare large"]/a/@href').extract()
        friends = [f.strip("/") for f in friends]
        # friends=hxs.select('//div[@class="nameplate"]/h6/text()').extract()
        return friends

    # def getPage(self,url):
    #
    #     print "starting phantomjs"
    #     dr=webdriver.PhantomJS('/usr/bin/phantomjs')
    #     dr.get(url)
    #     sou=dr.page_source
    #     sou2=sou.encode('ascii','ignore')
    #     hxs = HtmlXPathSelector(text=sou2)
    #
    #     return hxs

    def getType(self,url):
        find_index = url.find("myspace.com/")
        if find_index >= 0:
            x = url[find_index:].split("/")
            urltype =  x[3]
        return x[3]

    def parse(self, response):

        item = MyspaceItem()

        urltype = self.getType(response.url)

        item["_id"] = self.get_id(response.url)

        # hxs = self.getPage(response.url)
        hxs = HtmlXPathSelector(response)
        friends = self.getFriends(hxs)


        if urltype == "in":
            print 'in',len(friends),friends
            item['infriends'] = friends
        else:
            print 'out',len(friends),friends
            item['outfriends'] = friends















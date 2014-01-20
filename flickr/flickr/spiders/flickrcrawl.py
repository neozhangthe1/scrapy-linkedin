from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
import pymongo
from ..items import FlickrItem
from bs4 import UnicodeDammit


class FlickrSpider(CrawlSpider):
    name = "flickr"
    allowed_domains = []
    # g_ = open('id_lists.dat', 'r')
    mongo = pymongo.Connection("10.1.1.111", 12345)["flickr"]["profiles"]
    start_urls = []

    method = 1
    """
    crawl seed profile
    """
    if method == 0:
        res = mongo.find()
        for item in res:
            start_urls.append('http://www.flickr.com/people/' + item["_id"] + '/contacts/')
    start_urls = start_urls[1000:]

    """
    crawl all friends
    """
    if method == 1:
        item_set = set()
        res = mongo.find()
        for item in res:
            if "friend" in item:
                for f in item["friend"]:
                    item_set.add(f)
        for item in item_set:
            start_urls.append('http://www.flickr.com/people/' + item + '/contacts/')

    if method == 2:
        mongo = pymongo.Connection("10.1.1.111", 12345)["flickr"]["profiles_seed"]
        res = mongo.find()
        for item in res:
            start_urls.append('http://www.flickr.com/people/' + item["_id"] + '/contacts/')

    # # f_in = open("/Users/yutao/Documents/Data/NetworkIntegration/MultiSNS/multiple_flickr.csv","r")
# for e in f_in:
#     x = e.split(",")[1]
#     print x
#     start_urls.append('http://www.flickr.com/people/' + x.strip('"') + '/contacts/')

# rules = (Rule(SgmlLinkExtractor(allow=[r'/people/.*/contacts/\?filter=.*']),callback='parse'),)

    def parse(self, response):
        self.log('Hi, this is: %s' % response.url)
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//tr/td[@class = "Who"]')
        pname = UnicodeDammit((hxs.select('//span[@class = "nickname"]/text()').extract())[0]).markup

        try:
            page = int(hxs.select('//div[@class = "Pages"]/@data-page-count').extract()[0])
        except:
            page = 1

        item = FlickrItem()
        item['_id'] = self.get_username(response.url)
        item['pname'] = item["_id"]
        item['friend'] = []
        for site in sites:
            f = site.select('p/a[@rel="contact"]/@href').extract()[0].replace("photos","").replace("/","")
            item['friend'].append(f)
            print f
        yield item

        for p in range(1, page):
            if p == 1:
                p += 1
            url = 'http://www.flickr.com/people/' + pname + '/contacts/?filter&page=' + str(p)
            yield Request(url, callback=self.parse)

    def get_username(self, url):
        find_index = url.find("flickr.com/people/")
        if find_index >= 0:
            x = url[find_index:].split("/")
            return x[2]
        return None
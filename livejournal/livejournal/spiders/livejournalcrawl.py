from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
import pymongo

from ..items import LivejournalItem


class LiveJournalSpider(CrawlSpider):
    name = "livejournal"
    allowed_domains = []
    # g_ = open('id_lists.dat', 'r')
    start_urls = []
    # for e in g_:
    #     start_urls.append('http://www.' + e.strip() + '.livejournal.com/profile')

    mongo = pymongo.Connection("10.1.1.111", 12345)["livejournal"]["profiles"]
    # start_urls = []

    method = 1
    """
    crawl seed profile
    """
    if method == 0:
        res = mongo.find()
        for item in res:
            start_urls.append('http://' + item["_id"] + '.livejournal.com/profile')
            # start_urls.append('http://www.flickr.com/people/' + item["_id"] + '/contacts/')

    """
    crawl all friends
    """
    if method == 1:
        seed_set = set()
        item_set = set()
        res = mongo.find()
        for item in res:
            seed_set.add(res["_id"])
            if "friend" in item:
                for f in item["friend"]:
                    item_set.add(f)
        for item in item_set - seed_set:
            start_urls.append('http://' + item + '.livejournal.com/profile')
            # start_urls.append('http://www.flickr.com/people/' + item + '/contacts/')
    print len(start_urls), "to crawl"

    def parse(self, response):
        self.log('Hi, this is: %s' % response.url)
        hxs = HtmlXPathSelector(response)

        nomore = False

        try:
            more_url = (hxs.select('//a[@class = "b-friendslist-more"]/@href').extract())[0].decode('utf-8')
        except:
            nomore = True

        if nomore == True:
            item = LivejournalItem()
            item['url'] = response.url
            item['_id'] = self.get_username(response.url)
            item['pname'] = self.get_username(response.url)
            item['friend'] = []
            item['friend'].extend(hxs.select('//a[@class = " b-profile-username  "]/text()').extract())
            print item['pname'], item['friend']
            yield item
        else:
            url = more_url
            yield Request(url, callback=self.parse)


    def get_username(self, url):
        x = url.split(".")[0].split("//")[1]
        return x


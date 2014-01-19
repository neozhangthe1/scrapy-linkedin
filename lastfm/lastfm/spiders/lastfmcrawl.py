from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
import pymongo
from ..items import LastfmItem

class LastfmSpider(CrawlSpider):
    name = "lastfm"
    allowed_domains = []
    # g_ = open('id_lists.dat', 'r')
    # start_urls = []
    # for e in g_:
    #     start_urls.append('http://cn.last.fm/user/' + e.strip() + '/friends')
    mongo = pymongo.Connection("10.1.1.111", 12345)["lastfm"]["profiles"]
    start_urls = []
    # for e in g_:
    #     start_urls.append('https://myspace.com/'+e.strip()+'/connections/in')
    #     start_urls.append('https://myspace.com/'+e.strip()+'/connections/out')
    #
    method = 1
    """
    crawl seed profile
    """
    if method == 0:
        res = mongo.find()
        for item in res:
            # start_urls.append('https://myspace.com/'+item["_id"]+'/connections/in')
            # start_urls.append('https://myspace.com/'+item["_id"]+'/connections/out')
            start_urls.append('http://cn.last.fm/user/' + item["_id"] + '/friends')
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
            start_urls.append('http://cn.last.fm/user/' + item + '/friends')
            # start_urls.append('http://' + item + '.livejournal.com/profile')
            # start_urls.append('http://www.flickr.com/people/' + item + '/contacts/')
    print len(start_urls), "to crawl"


    # rules = (Rule(SgmlLinkExtractor(allow=[r'/people/.*/contacts/\?filter=.*']),callback='parse'),)

    def parse(self, response):
        self.log('Hi, this is: %s' % response.url)
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//div[@class="userContainer"]/div/strong/a/text()').extract()
        # pname = (hxs.select('//span[@class = "nickname"]/text()').extract())[0].decode('utf-8')

        try:
            try:
                page = int(hxs.select('//a[@class = "pagelink lastpage"]/text()').extract()[0])
                print page
            except:
                page = int(hxs.select('//span[@class = "selected"]/text()').extract()[0])
                print page
        except:
            page = 1
            print 'ex',page

        item = LastfmItem()
        item['_id'] = self.get_username(response.url)
        item['pname'] = item["_id"]
        item['friend'] = []

        name = self.get_username(response.url)
        print self.get_username(response.url)
        for site in sites:
            item['friend'].append(site)
            print site
        yield item


        for p in range(1, page):
            url = 'http://cn.last.fm/user/' + name + '/friends?page=' + str(p)
            yield Request(url, callback=self.parse)

    def get_username(self, url):
        find_index = url.find("cn.last.fm/user/")
        if find_index >= 0:
            x = url[find_index:].split("/")
            return x[2]
        return None

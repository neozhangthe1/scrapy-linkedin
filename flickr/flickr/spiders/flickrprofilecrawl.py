from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
import pymongo
from ..items import FlickrProfileItem
from bs4 import UnicodeDammit


class FlickrprofileSpider(CrawlSpider):
    name = "flickrprofile"
    allowed_domains = []
    # g_ = open('id_lists.dat', 'r')
    mongo = pymongo.Connection("10.1.1.111", 12345)["flickr"]["profiles"]
    start_urls = []

    method = 0
    """
    crawl seed profile
    """
    if method == 0:
        res = mongo.find()
        for item in res:
            if "profile" in item:
                if item["profile"]:
                    continue
            start_urls.append('http://www.flickr.com/people/' + item["_id"] + '/')

    """
    crawl all friends
    """
    # if method == 1:
    #     item_set = set()
    #     res = mongo.find()
    #     for item in res:
    #         if "friend" in item:
    #             for f in item["friend"]:
    #                 item_set.add(f)
    #     for item in item_set:
    #         start_urls.append('http://www.flickr.com/people/' + item + '/')
    #
    # if method == 2:
    #     mongo = pymongo.Connection("10.1.1.111", 12345)["flickr"]["profiles_seed"]
    #     res = mongo.find()
    #     for item in res:
    #         start_urls.append('http://www.flickr.com/people/' + item["_id"] + '/contacts/')

    # # f_in = open("/Users/yutao/Documents/Data/NetworkIntegration/MultiSNS/multiple_flickr.csv","r")
# for e in f_in:
#     x = e.split(",")[1]
#     print x
#     start_urls.append('http://www.flickr.com/people/' + x.strip('"') + '/contacts/')

# rules = (Rule(SgmlLinkExtractor(allow=[r'/people/.*/contacts/\?filter=.*']),callback='parse'),)

    def parse(self, response):
        self.log('Hi, this is: %s' % response.url)
        hxs = Selector(response)
        dls = hxs.xpath('//div[@id = "a-bit-more-about"]/dl')

        item = FlickrProfileItem()
        # item['_id'] = self.get_username(response.url)
        _id = self.get_username(response.url)
        print _id

        item["_id"] = _id
        for dl in dls:
            if dl.xpath('dt/text()').extract()[0] == "Name:":
                given_name = ""
                family_name = ""

                try:
                    given_name = dl.xpath('dd/span[@class="given-name"]/text()').extract()[0]
                except:
                    pass
                else:
                    print 'given_name:',given_name
                    # item['given_name'] = given_name

                try:
                    family_name = dl.xpath('dd/span[@class = "family-name"]/text()').extract()[0]
                except:
                    pass
                else:
                    print 'family_name:',family_name
                    # item['family_name'] = family_name
                item["name"] = given_name+" "+family_name

            if dl.xpath('dt/text()').extract()[0] == "Joined:":
                joined = dl.xpath('dd/text()').extract()[0]
                print 'joined time:', joined
                item['joined'] = joined

            if dl.xpath('dt/text()').extract()[0] == "Hometown:":
                home = dl.xpath('dd/text()').extract()[0]
                print 'hometown:',home
                item['hometown'] = home

            if dl.xpath('dt/text()').extract()[0] == "Currently:":
                try:
                    locality = dl.xpath('dd/span[@class = "adr"]/span[@class = "locality"]/text()').extract()[0]
                except:
                    pass
                else:
                    print 'locality:',locality
                    item['location'] = locality

                try:
                    country_name = dl.xpath('dd/span[@class = "adr"]/span[@class = "country-name"]/text()').extract()[0]
                except:
                    pass
                else:
                    print 'country-name:',country_name
                    item['country'] = country_name

            if dl.xpath('dt/text()').extract()[0] == "I am:":
                gender = dl.xpath('dd/text()').extract()[0].strip()
                print 'gender:', gender
                item['gender'] = gender

            if dl.xpath('dt/text()').extract()[0] == "Occupation:":
                occupation = dl.xpath('dd/text()').extract()[0]
                print 'occupation:',occupation
                item['occupation'] = occupation

            if dl.xpath('dt/text()').extract()[0] == "Website:":
                websitename = dl.xpath('dd/a/text()').extract()[0]
                websiteurl = dl.xpath('dd/a/@href').extract()[0]
                print 'website:',websitename,websiteurl
                item['websitename'] = websitename
                item['websiteurl'] = websiteurl
        yield item


    def get_username(self, url):
        find_index = url.find("flickr.com/people/")
        if find_index >= 0:
            x = url[find_index:].split("/")
            return x[2]
        return None
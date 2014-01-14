from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request

from ..items import FlickrItem


class FlickrSpider(CrawlSpider):
    name = "flickr"
    allowed_domains = []
    g_ = open('id_lists.dat', 'r')
    start_urls = []
    for e in g_:
        start_urls.append('http://www.flickr.com/people/' + e.strip() + '/contacts/')

    # rules = (Rule(SgmlLinkExtractor(allow=[r'/people/.*/contacts/\?filter=.*']),callback='parse'),)


    def parse(self, response):
        self.log('Hi, this is: %s' % response.url)
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//tr/td[@class = "Who"]')
        pname = (hxs.select('//span[@class = "nickname"]/text()').extract())[0].decode('utf-8')
        page = int(hxs.select('//div[@class = "Pages"]/@data-page-count').extract()[0])

        for site in sites:
            item = FlickrItem()
            item['pname'] = pname
            item['friend'] = site.select('h2/text()').extract()
            print site.select('h2/text()').extract()
            yield item.load_item()

        for p in range(1, page):
            if p == 1:
                p += 1
            url = 'http://www.flickr.com/people/' + pname + '/contacts/?filter&page=' + str(p)
            yield Request(url, callback=self.parse)


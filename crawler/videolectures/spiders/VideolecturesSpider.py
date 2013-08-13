from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy import log
from videolectures.items import LinkedinItem, PersonProfileItem
from os import path
from videolectures.parser.HtmlParser import HtmlParser
import os
import urllib
import string
from bs4 import UnicodeDammit
from videolectures.db import MongoDBClient
import pymongo

class VideolecturesSpider(CrawlSpider):
    name = 'VideolecturesSpider'
    allowed_domains = ['videolectures.net']
    #start_urls = [ "http://videolectures.net/site/list/authors/?page=%s" % s for s in [20,21]]

    rules = (
        #Rule(SgmlLinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def __init__(self):
        self.url_collection = pymongo.Connection("10.1.1.111",12345)["videolectures"]["urls"]
        self.start_urls = []
        for data in self.url_collection.find({}):
            for u in data["urls"]:
                if u["flag"] == 0:
                    self.start_urls.append(u["u"])
        print len(self.start_urls), "to crawl"
        
    def parse(self, response):
        """
        default parse method, rule is not useful now
        """
        #response = response.replace(url=HtmlParser.remove_url_parameter(response.url))
        hxs = HtmlXPathSelector(response)
        index_level = self.determine_level(response)
        if index_level == 1:
            #self.save_to_file_system(index_level, response)
            page = int(response.url[response.url.find("?page=")+6:])
            relative_urls = self.get_follow_links(index_level, hxs)
            item = {"_id":page, "urls":[{"u":u, "flag":0} for u in relative_urls]}
            self.url_collection.insert(item)
            if relative_urls is not None:
                for url in relative_urls:
                    yield Request(url, callback=self.parse)
        elif index_level == 2:
            personProfile = HtmlParser.extract_videolectures_profile(hxs)
            videolectures_id = self.get_videolectures_id(response.url)
            #videolectures_id = UnicodeDammit(urllib.unquote_pblus(linkedin_id)).markup
            if videolectures_id:
                personProfile['_id'] = videolectures_id
                personProfile['url'] = UnicodeDammit(response.url).markup
                yield personProfile
    
    def determine_level(self, response):
        """
        determine the index level of current response, so we can decide wether to continue crawl or not.
        level 1: site/list/authors/
        level 2: person page
        level 3: lecture page
        level 4: org
        level 5: conference
        """
        import re
        url = response.url
        if re.match(".+/site/list/authors", url):
            return 1
        else:
            return 2
        #elif re.match(".+/[A-Z]\d+.html", url):
        #    return 2
        #elif re.match(".+/people/[a-zA-Z0-9-]+.html", url):
        #    return 3
        #elif re.match(".+/pub/dir/.+", url):
        #    return 4
        #elif re.match(".+/search/._", url):
        #    return 4
        #elif re.match(".+/pub/.+", url):
        #    return 5
        return None
    
    def save_to_file_system(self, level, response):
        """
        save the response to related folder
        """
        if level in [1, 2, 3, 4, 5]:
            fileName = self.get_clean_file_name(level, response)
            if fileName is None:
                return
            
            fn = path.join(self.settings["DOWNLOAD_FILE_FOLDER"], str(level), fileName)
            self.create_path_if_not_exist(fn)
            if not path.exists(fn):
                with open(fn, "w") as f:
                    f.write(response.body)
    
    def get_clean_file_name(self, level, response):
        """
        generate unique linkedin id, now use the url
        """
        url = response.url
        if level in [1, 2, 3]:
            return url.split("/")[-1]
        
        videolectures_id = self.get_videolectures_id(url)
        if videolectures_id:
            return videolectures_id
        return None
        
    def get_videolectures_id(self, url):
        find_index = url.find("videolectures.net/")
        if find_index >= 0:
            return url[find_index+18:].replace('/', '')
        return None
        
    def get_follow_links(self, level, hxs):
        if level == 1:
            relative_urls = hxs.select("//tr/td[@align='right']/b/a/@href").extract()
            relative_urls = ["http://videolectures.net" + x for x in relative_urls]
            print len(relative_urls), "person to crawl"
        #if level in [1, 2, 3]:
        #    relative_urls = hxs.select("//ul[@class='directory']/li/a/@href").extract()
            
        #    return relative_urls
        #elif level == 4:
        #    relative_urls = relative_urls = hxs.select("//ol[@id='result-set']/li/h2/strong/a/@href").extract()
        #    relative_urls = ["http://linkedin.com" + x for x in relative_urls]
        return relative_urls

    def create_path_if_not_exist(self, filePath):
        if not path.exists(path.dirname(filePath)):
            os.makedirs(path.dirname(filePath))
            

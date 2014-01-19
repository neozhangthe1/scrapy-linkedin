# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class FlickrItem(Item):
    # define the fields for your item here like:
    _id = Field()
    pname = Field()
    friend = Field()


class FlickrProfileItem(Item):
    _id = Field()
    profile = Field()
    name = Field()
    location = Field()
    hometown = Field()
    gender = Field()
    status = Field()
    occupation = Field()
    links = Field()
    connections = Field()
    aboutme = Field()

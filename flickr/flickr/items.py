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


class PersonProfileItem(Item):
    _id = Field()
    url = Field()
    name = Field()
    also_view = Field()
    education = Field()
    locality = Field()
    industry = Field()
    summary = Field()
    specilities = Field()
    skills = Field()
    interests = Field()
    group = Field()
    honors = Field()
    education = Field()
    experience = Field()
    overview_html = Field()
    homepage = Field()

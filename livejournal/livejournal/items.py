# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class LivejournalItem(Item):
    # define the fields for your item here like:
    # name = Field()
    _id = Field()
    pname = Field()
    url = Field()
    friend = Field()


class LivejournalProfileItem(Item):
    name = Field()
    birthdate = Field()
    location = Field()
    links = Field()
    bio = Field()
    email = Field()
    schools = Field()
    interests = Field()

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
from scrapy import log
from items import FlickrProfileItem


class FlickrPipeline(object):
    def process_item(self, item, spider):
        return item


# Copyright 2011 Julien Duponchelle <julien@duponchelle.info>.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
class MongoDBPipeline(object):
    def __init__(self):
        import pymongo

        connection = pymongo.Connection(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        self.db = connection[settings['MONGODB_DB']]
        self.collection = self.db[settings['MONGODB_COLLECTION']]
        if self.__get_uniq_key() is not None:
            self.collection.create_index(self.__get_uniq_key(), unique=True)

    def process_item(self, item, spider):
        if self.__get_uniq_key() is None:
            self.collection.insert(dict(item))
        else:
            old_item = self.collection.find_one({"_id": item["_id"]})
            if type(item) is FlickrProfileItem:
                print "Append profile for", item["_id"]
                for k in item:
                    old_item[k] = item[k]
                old_item["profile"] = True
            else:
                print "Append friend for", item["_id"]
                if old_item is not None:
                    if "friend" in old_item:
                        friends = set(old_item["friend"])
                        for f in item["friend"]:
                            friends.add(f)
                        old_item["friend"] = list(friends)
                    else:
                        old_item["friend"] = item["friend"]
                else:
                    old_item = dict(item)
            self.collection.update(
                {self.__get_uniq_key(): item[self.__get_uniq_key()]},
                old_item,
                upsert=True)
        log.msg("Item wrote to MongoDB database %s/%s" %
                (settings['MONGODB_DB'], settings['MONGODB_COLLECTION']),
                level=log.DEBUG, spider=spider)
        return item

    def __get_uniq_key(self):
        if not settings['MONGODB_UNIQ_KEY'] or settings['MONGODB_UNIQ_KEY'] == "":
            return None
        return settings['MONGODB_UNIQ_KEY']
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
from scrapy import log

class MyspacePipeline(object):
    def process_item(self, item, spider):
        return item

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
            print "Append friend for", item["_id"]
            old_item = self.collection.find_one({"_id": item["_id"]})
            in_edges = set()
            out_edges = set()
            #crawl infriends first,if _id exists, add outfriends to the item
            if old_item is not None:
                if "infriend" in old_item:
                    for f in old_item["infriend"]:
                        in_edges.add(f)
                if "outfriend" in old_item:
                    for f in old_item["outfriend"]:
                        out_edges.add(f)
                if "infriend" in item:
                    for f in item["infriend"]:
                        in_edges.add(f)
                if "outfriend" in item:
                    for f in item["outfriend"]:
                        out_edges.add(f)
                old_item["infriend"] = list(in_edges)
                old_item["outfriend"] = list(out_edges)
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

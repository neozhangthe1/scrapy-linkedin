__author__ = 'yutao'
import pymongo


def transfer():
    mongo_src = pymongo.Connection("10.1.1.110", 27017)["scrapy"]["person_profiles_1221"]
    mongo_tar = pymongo.Connection("10.1.1.111", 12345)["linkedin"]["profiles"]
    res = mongo_src.find()
    for item in res:
        print item["_id"]
        if "also_view" in item:
            friends = []
            for f in item["also_view"]:
                tmp = {"url": f["linkedin_id"], "id": f["url"]}
                friends.append(tmp)
            item["also_view"] = friends
        else:
            item["also_view"] = []
        try:
            mongo_tar.save(item)
        except:
            pass

if __name__ == "__main__":
    transfer()
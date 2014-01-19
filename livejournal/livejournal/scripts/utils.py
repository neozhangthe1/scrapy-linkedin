__author__ = 'yutao'
import MySQLdb
import pymongo
from bs4 import UnicodeDammit


def transfer():
    con = MySQLdb.connect(host="10.1.1.110", user="root", passwd="keg2012", db="multions")
    cur = con.cursor()
    mongo = pymongo.Connection("10.1.1.111", 12345)["livejournal"]["profiles"]
    query = "select id from multiple_livejournal"
    cur.execute(query)
    for row in cur.fetchall():
        print row[0]
        res = mongo.find_one({"_id": row[0]})
        if res is not None:
            res["seed"] = True
            mongo.save(res)
        else:
            res = {"seed":True, "_id":row[0]}
            mongo.save(res)


def clean():
    mongo = pymongo.Connection("10.1.1.111", 12345)["livejournal"]["profiles"]
    res = mongo.find()
    for item in res:
        if "friend" in item:
            friend = item["friend"]
            if len(friend) == 1:
                item["friend"] = friend[0]
        else:
            item["friend"] = []
        mongo.save(item)

def transfer_gplus():
    con = MySQLdb.connect(host="10.1.1.110", user="root", passwd="keg2012", db="multions")
    cur = con.cursor()
    mongo = pymongo.Connection("10.1.1.111", 12345)["gplus"]["profiles"]
    query = "select id from multiple_picasaweb"
    cur.execute(query)
    for row in cur.fetchall():
        print row[0]
        res = mongo.find_one({"_id": row[0]})
        if res is not None:
            res["seed"] = True
            mongo.save(res)
        else:
            res = {"seed":True, "_id":row[0]}
            mongo.save(res)

def transfer_livejournal():
    con = MySQLdb.connect(host="10.1.1.110", user="root", passwd="keg2012", db="multions")
    cur = con.cursor()
    mongo = pymongo.Connection("10.1.1.111", 12345)["livejournal"]["profiles_seed_content"]
    query = "select * from multiple_livejournal"
    cur.execute(query)
    for row in cur.fetchall():
        print row[0]
        res = mongo.find_one({"_id": row[1]})
        if res is None:
            res = {"seed":True, "_id": row[1]}
        res["seed"] = True
        res["gid"] = row[0]
        res["name"] = UnicodeDammit(row[2]).markup
        res["birthdate"] = row[3]
        res["location"] = UnicodeDammit(row[4]).markup
        res["links"] = row[5]
        res["connections"] = row[6]
        res["aboutme"] = row[7]
        res["email"] = row[8]
        res["schools"] = UnicodeDammit(row[9]).markup
        res["interests"] = row[10]
        mongo.save(res)


def transfer_flickr():
    con = MySQLdb.connect(host="10.1.1.110", user="root", passwd="keg2012", db="multions")
    cur = con.cursor()
    mongo = pymongo.Connection("10.1.1.111", 12345)["flickr"]["profiles_seed_content"]
    query = "select * from multiple_flickr"
    cur.execute(query)
    for row in cur.fetchall():
        print row[0]
        res = mongo.find_one({"_id": row[1]})
        if res is None:
            res = {"seed":True, "_id": row[1]}
        res["seed"] = True
        res["gid"] = row[0]
        res["name"] = UnicodeDammit(row[2]).markup
        res["location"] = row[3]
        res["hometown"] = row[4]
        res["gender"] = row[5]
        res["status"] = row[6]
        res["occupation"] = row[7]
        res["links"] = row[8]
        res["connections"] = row[10]
        res["aboutme"] = row[11]
        mongo.save(res)


def transfer_facebook():
    con = MySQLdb.connect(host="10.1.1.110", user="root", passwd="keg2012", db="multions")
    cur = con.cursor()
    mongo = pymongo.Connection("10.1.1.111", 12345)["facebook"]["profiles"]
    query = "select * from multiple_facebook"
    cur.execute(query)
    for row in cur.fetchall():
        print row[0]
        res = mongo.find_one({"_id": row[2]})
        if res is None:
            res = {"seed":True, "_id": row[2]}
        res["seed"] = True
        res["gid"] = row[0]
        res["did"] = row[1]
        res["name"] = row[3]
        res["gender"] = row[4]
        res["links"] = row[5]
        res["location"] = row[6]
        res["hometown"] = row[7]
        res["phone"] = row[8]
        res["interested_in"] = row[9]
        res["language"] = row[10]
        res["schools"] = row[11]
        res["companies"] = row[12]
        res["status"] = row[13]
        res["email"] = row[14]
        res["birthdate"] = row[15]
        res["religion"] = row[16]
        res["relatives"] = row[17]
        res["political"] = row[18]
        res["connections"] = row[19]
        res["interests"] = row[20]
        res["anniversary"] = row[21]
        res["aboutme"] = row[22]
        res["sport"] = row[23]
        res["music"] = row[24]
        res["tv"] = row[25]
        res["movies"] = row[26]
        res["books"] = row[27]
        res["quote"] = row[28]
        res["age_group"] = row[29]
        mongo.save(res)




def transfer_lastfm():
    con = MySQLdb.connect(host="10.1.1.110", user="root", passwd="keg2012", db="multions")
    cur = con.cursor()
    mongo = pymongo.Connection("10.1.1.111", 12345)["lastfm"]["profiles"]
    query = "select * from multiple_lastfm"
    cur.execute(query)
    for row in cur.fetchall():
        print row[0]
        res = mongo.find_one({"_id": row[1]})
        if res is None:
            res = {"seed":True, "_id": row[1]}
        res["seed"] = True
        res["gid"] = row[0]
        res["name"] = row[2]
        res["age"] = row[3]
        res["gender"] = row[4]
        res["location"] = row[6]
        res["links"] = row[7]
        res["aboutme"] = row[8]
        res["connections"] = row[9]
        res["music"] = row[10]
        mongo.save(res)


def transfer_myspace():
    con = MySQLdb.connect(host="10.1.1.110", user="root", passwd="keg2012", db="multions")
    cur = con.cursor()
    mongo = pymongo.Connection("10.1.1.111", 12345)["myspace"]["profiles"]
    query = "select * from multiple_myspace"
    cur.execute(query)
    for row in cur.fetchall():
        print row[0]
        res = mongo.find_one({"_id": row[1]})
        if res is None:
            res = {"seed":True, "_id": row[1]}
        res["seed"] = True
        res["gid"] = row[0]
        res["name"] = row[2]
        res["age"] = row[3]
        res["gender"] = row[4]
        res["links"] = row[5]
        res["status"] = row[7]
        res["interest"] = row[8]
        res["hometown"] = row[9]
        res["orientation"] = row[10]
        res["bodytype"] = row[11]
        res["ethnicity"] = row[12]
        res["religion"] = row[13]
        res["sign"] = row[14]
        res["children"] = row[15]
        res["smokedrink"] = row[16]
        res["education"] = row[17]
        res["occupation"] = row[18]
        res["income"] = row[19]
        res["schools"] = row[20]
        res["connections"] = row[21]
        res["aboutme"] = row[22]
        mongo.save(res)


def transfer_twitter():
    con = MySQLdb.connect(host="10.1.1.110", user="root", passwd="keg2012", db="multions")
    cur = con.cursor()
    mongo = pymongo.Connection("10.1.1.111", 12345)["twitter"]["profiles_seed"]
    query = "select * from multiple_twitter"
    cur.execute(query)
    for row in cur.fetchall():
        print row[1]
        res = mongo.find_one({"_id": row[1]})
        if res is None:
            res = {"seed":True, "_id": row[1]}
        res["seed"] = True
        res["gid"] = row[0]
        res["name"] = row[2]
        res["location"] = row[3]
        res["links"] = row[4]
        res["aboutme"] = row[5]
        res["connections"] = row[7]
        mongo.save(res)



def transfer_twitter_txt():
    mongo = pymongo.Connection("10.1.1.111", 12345)["twitter"]["profiles"]
    f_in = open("/Users/yutao/Documents/Data/Twitter/twitter.40b.nodes")
    for line in f_in:
        x = line.strip().split(" ")
        item = {"_id":x[1], "idx":int(x[0])}
        mongo.save(item)

if __name__ == "__main__":
    transfer_facebook()

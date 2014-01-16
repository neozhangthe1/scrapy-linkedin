__author__ = 'yutao'
import MySQLdb
import pymongo


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


if __name__ == "__main__":
    transfer()

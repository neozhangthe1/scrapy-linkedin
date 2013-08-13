# Scrapy settings for linkedin project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
import os

BOT_NAME = 'videolectures'

SPIDER_MODULES = [BOT_NAME+'.spiders']
NEWSPIDER_MODULE = BOT_NAME+'.spiders'

DOWNLOADER_MIDDLEWARES = {
    BOT_NAME+'.middleware.CustomHttpProxyMiddleware': 543,
    BOT_NAME+'.middleware.CustomUserAgentMiddleware': 545,
}

########### Item pipeline
ITEM_PIPELINES = [
                  BOT_NAME+".pipelines.MongoDBPipeline",
]

MONGODB_SERVER = '10.1.1.111'
MONGODB_PORT = 12345
MONGODB_DB = BOT_NAME
MONGODB_COLLECTION = 'person_profiles'
MONGODB_UNIQ_KEY = '_id'
###########

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'linkedin (+http://www.yourdomain.com)'

# Enable auto throttle
AUTOTHROTTLE_ENABLED = True

COOKIES_ENABLED = False

# Set your own download folder
DOWNLOAD_FILE_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "download_file")



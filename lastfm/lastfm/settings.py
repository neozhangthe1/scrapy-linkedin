# Scrapy settings for lastfm project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os

BOT_NAME = 'lastfm'

SPIDER_MODULES = ['lastfm.spiders']
NEWSPIDER_MODULE = 'lastfm.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'lastfm (+http://www.yourdomain.com)'
########### Item pipeline

ITEM_PIPELINES = [
    "lastfm.pipelines.MongoDBPipeline",
]

# in
MONGODB_SERVER = '10.1.1.111'
#out
#MONGODB_SERVER = ''
MONGODB_PORT = 12345
# MONGODB_SERVER = 'localhost'
# MONGODB_PORT = 27017
MONGODB_DB = 'lastfm'
MONGODB_COLLECTION = 'profiles'
MONGODB_UNIQ_KEY = '_id'
##########

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'linkedin (+http://www.yourdomain.com)'

# Enable auto throttle
AUTOTHROTTLE_ENABLED = True

COOKIES_ENABLED = False

# Set your own download folder
# DOWNLOAD_FILE_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "download_file")

SCHEDULER_MIDDLEWARES = {
    'scheduler_middlewares.DuplicatesFilterMiddleware': 500
}

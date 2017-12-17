# -*- coding: utf-8 -*-

BOT_NAME = 'invest_scrape'

SPIDER_MODULES = ['invest_scrape.spiders']
NEWSPIDER_MODULE = 'invest_scrape.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Uncomment to remove DEBUG from log
#LOG_LEVEL='INFO'

# Uncomment to print log to 'mylog.txt'
#LOG_FILE = 'mylog.txt'

# Uncomment to add print statements to log
#LOG_STDOUT = True

# Format is 'postgresql://username:password@domain/database'
POSTGRES_DB_URL = 'postgresql://joseph:password@localhost:5432/postgres'  # DB to connect to
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'random_useragent.RandomUserAgentMiddleware': 400
}

# List of useragents to avoid being blocked
USER_AGENT_LIST = "useragents.txt"
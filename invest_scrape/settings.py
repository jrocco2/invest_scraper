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

# ITEM_PIPELINES = {
#    'invest_scrape.pipelines.InvestingScraperPipeline': 300,
# }

# Format is 'postgresql://username:password@domain/database'
POSTGRES_DB_URL = 'postgresql://joseph:password@localhost:5432/postgres'  # DB to connect to
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
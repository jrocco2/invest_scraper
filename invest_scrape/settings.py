# -*- coding: utf-8 -*-

# Scrapy settings for invest_scrape project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'invest_scrape'

SPIDER_MODULES = ['invest_scrape.spiders']
NEWSPIDER_MODULE = 'invest_scrape.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

#LOG_LEVEL='INFO'
#LOG_FILE = 'mylog.txt'
#LOG_STDOUT = True
ITEM_PIPELINES = {
   'invest_scrape.pipelines.InvestingScraperPipeline': 300,
}


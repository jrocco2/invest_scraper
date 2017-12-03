import scrapy
from invest_scrape.items import NewsScraperItem
from datetime import datetime, timedelta
import re

class NewsScrape(scrapy.Spider):
    name = "news_scrape"

    custom_settings = {
        'ITEM_PIPELINES': {'invest_scrape.pipelines.NewsScraperPipeline': 300}
    }
    # First Start Url
    start_urls = ["https://www.investing.com/news/stock-market-news"]

    def parse(self, response):
        item = NewsScraperItem()
        containers = response.xpath("//div[contains(@class,'largeTitle')]/article[contains(@class,"
                                    "'articleItem')]/div[contains(@class,'textDiv')]")
        for info in containers:

            date = info.xpath(".//div[contains(@class,'articleDetails')]/span[contains(@class,'date')]/text()").extract_first()
            date = re.sub(r'\xa0-\xa0', '', date)
            # Convert minutes ago to datetime
            date = datetime.now() - timedelta(minutes=int(re.sub(r'[^0-9]', '', date)))  # Regex = Where not numeric
            item['date'] = date.strftime("%Y/%m/%d %H:%M:%S")
            earn_id = re.search(r'[0-9]{4,}', info.xpath(".//a/@onclick").extract_first())
            item['id'] = earn_id.group()
            item['title'] = info.xpath(".//a/text()").extract_first()
            item['author'] = info.xpath(".//div[contains(@class,'articleDetails')]/span/text()").extract_first()
            item['text'] = info.xpath(".//p/text()").extract_first()
            item['link'] = info.xpath(".//a/@href").extract_first()

            yield item


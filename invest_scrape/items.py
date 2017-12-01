import scrapy

class InvestingScraperItem(scrapy.Item):
    """
    The fields that will be scraped from the website
    """
    id = scrapy.Field()
    date = scrapy.Field()
    currency = scrapy.Field()
    volatility = scrapy.Field()
    event = scrapy.Field()
    actual = scrapy.Field()
    forecast = scrapy.Field()
    previous = scrapy.Field()

    def __str__(self):
        """
        Overload the print method to avoid printing too many details in the log
        """
        return ""

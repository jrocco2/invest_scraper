import scrapy


class InvestingScraperItem(scrapy.Item):
    """
    Define the fields that will be sent to the Postgres DB
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
        Overload the print method to avoid printing to0 many details in the log
        """
        return ""

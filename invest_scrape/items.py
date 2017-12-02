import scrapy

class InvestingScraperItem(scrapy.Item):
    """
    The fields that will be scraped from the website
    """
    id = scrapy.Field()
    date = scrapy.Field()
    currency = scrapy.Field()
    importance = scrapy.Field()
    event = scrapy.Field()
    actual = scrapy.Field()
    actual_unit = scrapy.Field()
    forecast = scrapy.Field()
    forecast_unit = scrapy.Field()
    previous = scrapy.Field()
    previous_unit = scrapy.Field()

    # def __str__(self):
    #     """
    #     Overload the print method to avoid printing too many details in the log
    #     """
    #     return ""

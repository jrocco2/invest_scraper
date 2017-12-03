import scrapy

class InvestingScraperItem(scrapy.Item):
    """
    Scraper item for economic calendar
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


class EarningScraperItem(scrapy.Item):
    """
    Scraper item for earnings calendar
    """
    id = scrapy.Field()
    date = scrapy.Field()
    country = scrapy.Field()
    company = scrapy.Field()
    short_code = scrapy.Field()
    eps_actual = scrapy.Field()
    eps_forecast = scrapy.Field()
    rev_actual = scrapy.Field()
    rev_actual_units = scrapy.Field()
    rev_forecast = scrapy.Field()
    rev_forecast_units = scrapy.Field()
    market_cap = scrapy.Field()
    market_time = scrapy.Field()


class NewsScraperItem(scrapy.Item):
    """
    Scraper item for earnings calendar
    """
    id = scrapy.Field()
    date = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    text = scrapy.Field()
    link = scrapy.Field()